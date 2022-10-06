import numpy as np
from matplotlib import pyplot as plt

from utils import get_start_end_time, to_minutes_since_start

colours = ["b", "g", "r", "c"]


def plot_count_over_time(teams, title):
    start_time, end_time = get_start_end_time(teams)
    end_time = to_minutes_since_start(start_time, end_time)

    for i, (team, colour) in enumerate(zip(teams, colours)):
        time_of_chats = to_minutes_since_start(start_time, team[:, 0])
        time_index = np.digitize(time_of_chats, [i for i in range(int(end_time) + 1)])
        time, counts = np.unique(time_index, return_counts=True)
        plt.plot(time, counts, color=colour, label=f"Team {i + 1}")

    plt.title(title)
    plt.xlabel("time (min)")
    plt.ylabel("count")
    plt.legend()
    plt.show()


def plot_counts_by_team_and_member(teams, title):
    member_counts = {}
    for team_no, team in enumerate(teams):
        members, team_member_counts = np.unique(team[:, 1], return_counts=True, axis=0)
        for i, count in enumerate(team_member_counts):
            if i in member_counts:
                member_counts[i].append(count)
            else:
                member_counts[i] = [*[0 for _ in range(team_no)], count]

        for i in range(len(member_counts) - len(team_member_counts)):
            member_counts[len(team_member_counts) + i].append(0)

    x = np.arange(len(teams))  # the label locations
    width = 0.35 / len(member_counts)
    fig, ax = plt.subplots()
    bars = []
    for i, member_id in enumerate(member_counts):
        bars.append(
            ax.bar(x + (i * width), member_counts[member_id], width, label=f"Member {member_id}"))

    ax.set_ylabel('Counts')
    ax.set_title(title)
    ax.set_xticks(x, [f"Team {i + 1}" for i in range(len(teams))])
    ax.legend()

    _ = [ax.bar_label(bar, padding=3) for bar in bars]

    fig.tight_layout()

    plt.show()


def plot_counts_by_question_type(teams, title, question_time_bins, category_names, question_type_names):
    activity = []

    for category in question_time_bins:
        # {team_no : [bin_1_count, bin_2_count, ...]}
        category_counts = {}
        for i, team in enumerate(teams):
            category_counts[i] = []
            for start, end in category:
                chats = team[np.logical_and(start < team[:, 0], team[:, 0] < end), :]
                duration = to_minutes_since_start(start, end)
                category_counts[i].append(round(len(chats)/duration, 2))
        activity.append(category_counts)

    fig, ax = plt.subplots(2, len(activity) // 2)
    if len(ax.shape) == 1:
        ax = ax[:, np.newaxis]
    for activity_no in range(len(activity)):
        ax_x = activity_no % 2
        ax_y = activity_no // 2

        x = np.arange(len(question_type_names))
        width = 0.35 / len(question_type_names)
        bars = []
        for i, team_id in enumerate(activity[activity_no]):
            bars.append(
                ax[ax_x, ax_y].bar(x + (i * width), activity[activity_no][team_id], width, label=f"Team {team_id}"))

        ax[ax_x, ax_y].set_ylabel('Counts / min')
        ax[ax_x, ax_y].set_title(category_names[activity_no])
        ax[ax_x, ax_y].set_xticks(x, [question_type for question_type in question_type_names])
        ax[ax_x, ax_y].legend()

        # _ = [ax[ax_x, ax_y].bar_label(bar, padding=3) for bar in bars]

    fig.tight_layout()
    fig.suptitle(title)
    plt.show()

