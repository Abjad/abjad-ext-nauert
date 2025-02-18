import abc
import multiprocessing
import pickle
import typing

from . import quantizationjob as _quantizationjob


class JobHandler(abc.ABC):
    """
    Abstact job-handler.

    ``JobHandlers`` control how ``QuantizationJob`` instances are processed by
    the ``quantize`` function, either serially or in parallel.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, jobs):
        """
        Calls job handler.
        """
        raise NotImplementedError


class ParallelJobHandlerWorker(multiprocessing.Process):
    """
    Parallel job-handler worker.

    Worker process which runs ``QuantizationJobs``.

    Not composer-safe.

    Used internally by ``ParallelJobHandler``.
    """

    ### INITIALIZER ###

    def __init__(self, job_queue=None, result_queue=None) -> None:
        multiprocessing.Process.__init__(self)
        job_queue = job_queue or ()
        result_queue = result_queue or ()
        self.job_queue = job_queue
        self.result_queue = result_queue

    ### PUBLIC METHODS ###

    def run(self) -> None:
        """
        Runs parallel job handler worker.
        """
        while True:
            job = None
            if hasattr(self.job_queue, "get"):
                job = self.job_queue.get()
            if job is None:
                # poison pill causes worker shutdown
                # print '{}: Exiting'.format(process_name)
                assert hasattr(self.job_queue, "task_done")
                self.job_queue.task_done()
                break
            # print '{}: {!r}'.format(process_name, job)
            job = pickle.loads(job)
            job()
            self.job_queue.task_done()
            assert hasattr(self.result_queue, "put")
            self.result_queue.put(pickle.dumps(job, protocol=0))
        return


class ParallelJobHandler(JobHandler):
    """
    Parallel job-handler.

    Processes ``QuantizationJob`` instances in parallel, based on the number of
    CPUs available.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(self, jobs):
        """
        Calls parallel job handler.
        """
        finished_jobs = []
        job_queue = multiprocessing.JoinableQueue()
        result_queue = multiprocessing.Queue()
        workers = [
            ParallelJobHandlerWorker(job_queue, result_queue)
            for i in range(multiprocessing.cpu_count() * 2)
        ]
        for worker in workers:
            worker.start()
        for job in jobs:
            job_queue.put(pickle.dumps(job, protocol=0))
        for i in range(len(jobs)):
            finished_jobs.append(pickle.loads(result_queue.get()))
        for worker in workers:
            job_queue.put(None)
        job_queue.join()
        result_queue.close()
        job_queue.close()
        for worker in workers:
            worker.join()
        return finished_jobs


class SerialJobHandler(JobHandler):
    """
    Serial job-handler.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __call__(
        self, jobs: typing.Sequence[_quantizationjob.QuantizationJob]
    ) -> typing.Sequence[_quantizationjob.QuantizationJob]:
        """
        Calls serial job handler.
        """
        for job in jobs:
            job()
        return jobs
