from plotting import plot_counts_by_question_type, plot_count_over_time, plot_counts_by_team_and_member
from utils import get_chat_data, get_talk_data


def handle_chats(filename, rounds, round_names, category_names):
    teams = get_chat_data(filename)
    plot_counts_by_question_type(teams, "Chat Count by question type and category", rounds, category_names, round_names)
    plot_count_over_time(teams, "Chat Count vs time for each team")
    plot_counts_by_team_and_member(teams, 'Chat count by team member')

def handle_talks(filename, rounds, round_names, category_names):
    teams = get_talk_data(filename)
    plot_counts_by_question_type(teams, "Talk Activity by question type and category", rounds, category_names, round_names)

    plot_count_over_time(teams, "Talk Activity vs time for each team")
    plot_counts_by_team_and_member(teams, 'Talk Activity by team member')


if __name__ == "__main__":
    rounds = [
        [[1664431635289, 1664431799384], [1664431799384, 1664431963479], [1664431963479, 1664432127574], [1664432127574, 1664432291670]],
        [[1664432678581, 1664432806428], [1664432806428, 1664432934275], [1664432934275, 1664433062122], [1664433062122 , 1664433189971]]
    ]
    round_names = ["picture", "category", "trivia", "who am i"]
    category_names = ["geography", "science"]

    handle_chats("chat_data_2.json", rounds, round_names, category_names)
    handle_talks("talk_data_2.json", rounds, round_names, category_names)


    # geography = 1664431635289 -> 1664432291670
        # picture = 1664431635289 -> 1664431799384
        # category = 1664431799384 -> 1664431963479
        # trivia = 1664431963479 -> 1664432127574
        # whoami = 1664432127574 -> 1664432291670
    # science = 1664432678581 -> 1664433189971
        # picture = 1664432678581 -> 1664432806428
        # category = 1664432806428 -> 1664432934275
        # trivia = 1664432934275 -> 1664433062122
        # whoami = 1664433062122 -> 1664433189971

