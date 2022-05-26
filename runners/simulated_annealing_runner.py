import matplotlib.pyplot as plt
from task_generator.task_scheduling_generator import UnrelatedParallelMachineSchedulingGenerator
from algorithms.simulated_annealing import SimulatedAnnealing
from algorithms.shortest_release_date import ShortestReleaseDates
from utils.utils import vectorize_solution, get_solution_cost, get_grouped_solution, initialize_solution
from utils.plotter import gantt_plot, plot_jobs


def main():
    scheduling_problem = UnrelatedParallelMachineSchedulingGenerator()
    SRD = ShortestReleaseDates()
    srd_solution = SRD.assign_jobs(scheduling_problem=scheduling_problem)
    srd_vector = vectorize_solution(machines=srd_solution.machines)
    srd_cost = get_solution_cost(scheduling_problem=scheduling_problem, vectorized_solution=srd_vector)
    print(f"SRD cost: {srd_cost}")

    plot_jobs(scheduling_solution=scheduling_problem)
    gantt_plot(scheduling_solution=srd_solution, title="SRD", plot_label=False)

    simulated_annealing = SimulatedAnnealing(
        temperature=1, cooling_rate=0.99, max_iterations=5000, display_iteration=True
    )
    simulated_annealing_solution = simulated_annealing.run(scheduling_problem=scheduling_problem)
    SA_solution, _ = initialize_solution(
        scheduling_problem=scheduling_problem,
        grouped_vectorized_solution=get_grouped_solution(simulated_annealing_solution.position),
    )
    gantt_plot(scheduling_solution=SA_solution, title="SA", plot_label=False)
    print(f"SA cost: {simulated_annealing_solution.cost}")

    plt.plot(simulated_annealing.bets_cost_history)
    plt.show()
    plt.semilogy(simulated_annealing.bets_cost_history)
    plt.show()


if __name__ == "__main__":
    main()
