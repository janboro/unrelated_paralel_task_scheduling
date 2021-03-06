from typing import List
import numpy as np
from algorithms.shortest_release_date import ShortestReleaseDates
from algorithms.random_solution import RandomSolution
from utils.utils import initialize_solution, vectorize_solution, get_grouped_solution


class Operators:
    def __init__(self):
        self.SRD = ShortestReleaseDates()
        self.random_solution = RandomSolution()

    def _fill_missing_fields(self, solution: List, scheduling_problem, fill_randomly: bool):
        grouped_solution = get_grouped_solution(solution)
        scheduling_problem, scheduled_jobs = initialize_solution(
            scheduling_problem=scheduling_problem,
            grouped_vectorized_solution=grouped_solution,
        )
        if fill_randomly:
            scheduling_problem = self.random_solution.assign_randomly(
                scheduling_problem=scheduling_problem, scheduled_jobs=scheduled_jobs
            )
        else:
            scheduling_problem = self.SRD.assign_jobs(
                scheduling_problem=scheduling_problem, scheduled_jobs=scheduled_jobs
            )
        return vectorize_solution(machines=scheduling_problem.machines)

    @staticmethod
    def _sort_subtraction(arr: List):
        """Sorting based on a bubble sort"""
        for i in range(len(arr)):
            for j in range(len(arr) - i - 1):
                if arr[j] == None and arr[j + 1] != None and arr[j + 1] != "*":
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr

    @staticmethod
    def _subtractor(arr_A: List, arr_B: List):
        result = []
        for i, j in zip(arr_A, arr_B):
            if i == j and i != "*":
                result.append(None)
            else:
                result.append(i)
        return result

    @staticmethod
    def _reversed_subtractor(arr_A: List, arr_B: List):
        result = []
        for i, j in zip(arr_A, arr_B):
            if i != j and i != "*":
                result.append(None)
            else:
                result.append(i)
        return result

    def subtract(self, arr_A: List, arr_B: List, scheduling_problem, fill_randomly: bool, reverse: bool):
        if reverse:
            subtraction = self._reversed_subtractor(arr_A=arr_A, arr_B=arr_B)
        else:
            subtraction = self._subtractor(arr_A=arr_A, arr_B=arr_B)
        subtraction = self._sort_subtraction(subtraction)
        subtraction = self._fill_missing_fields(
            solution=subtraction, scheduling_problem=scheduling_problem, fill_randomly=fill_randomly
        )
        return subtraction

    def _get_multiplication_vector(self, arr_A: List, arr_B: List) -> List[List]:
        result = []
        for i in range(len(arr_A)):
            if arr_B[i] == "*":
                result.append("*")
            elif arr_A[i] == 1:
                result.append(arr_B[i])
            else:
                result.append(None)
        return result

    def multiply(self, arr_A: List, arr_B: List, scheduling_problem, fill_randomly: bool):
        multiplication_vector = self._get_multiplication_vector(arr_A=arr_A, arr_B=arr_B)
        solution = self._fill_missing_fields(
            solution=multiplication_vector, scheduling_problem=scheduling_problem, fill_randomly=fill_randomly
        )
        return solution

    def add(self, arr_A: List, arr_B: List, fill_randomly: bool):
        grouped_solution = get_grouped_solution(arr=arr_A)
        group_to_select = np.random.randint(low=0, high=len(grouped_solution))

        # if fill_randomly:
        #     result = []
        #     buffer = []
        #     for i in grouped_solution:
        #         if i == group_to_select:
        #             result.append(grouped_solution[i])
        #         else:
        #             result.append([])
        #     self._fill_missing_fields()
        # else:
        result = []
        buffer = []
        for i in range(len(grouped_solution)):
            for job in grouped_solution[i]:
                if i == group_to_select:
                    result.append(job)
                elif job is not None:
                    result.append(-1)
                    buffer.append(job)
                else:
                    result.append(None)
            result.append("*")
        result.pop()

        jobs_to_schedule = [value for value in arr_B if value in buffer]

        for i in range(len(result)):
            if result[i] == -1:
                result[i] = jobs_to_schedule.pop(0)

        return result
