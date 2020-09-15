# native imports
import csv


def analysis_basic(infile: str):
    """basic analysis of proj, likes, comments"""
    total = 0
    sess_proj_added = 0
    proj_like = 0
    proj_comment = 0
    comment_like = 0
    all_three = 0
    was_like_given = 0
    total_likes = 0
    was_comment_given = 0
    comment_not_given = 0
    total_comments = 0

    with open(infile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        # print(reader.fieldnames)

        for row in reader:
            if row['\ufeffsession_id'] != "":
                total += 1

            if row["projects_added"] == "TRUE":
                sess_proj_added += 1
                if row["likes_given"] == "TRUE":
                    proj_like += 1
                if row['comment_given'] == "TRUE":
                    proj_comment += 1

            if row["likes_given"] == "TRUE":
                was_like_given += 1
                total_likes += int(row["session_likes_given"])
                if row['comment_given'] == "TRUE":
                    comment_like += 1
                    if row["projects_added"] == "TRUE":
                        all_three += 1

            if row['comment_given'] == "TRUE":
                was_comment_given += 1
                total_comments += int(row["session_comments_given"])
            if row['comment_given'] == "FALSE":
                comment_not_given += 1

        print("total sessions: ", total)
        print("sessions proj added: ", sess_proj_added)
        print("was like given: ", was_like_given)
        print("total likes given: ", total_likes)
        print("     average likes given: ", total_likes / total)
        print("     average likes if at least 1 like was given: ", total_likes / was_like_given)
        print("was comment given: ", was_comment_given, comment_not_given)
        print("     average comments given: ", total_comments / total)
        print("     average comments if at least 1 comment was given: ", total_likes / was_comment_given)
        print("intersection p/l ", proj_like, "p/c ", proj_comment, "l/c", comment_like, "all", all_three)


def session_times(infile: str):
    """analysis of session"""
    total_sess = 300
    total_duration = 0
    total_active_duration = 0
    total_inactive_duration = 0
    inactive_sess = 0
    min_active_duration = 200000
    max_active_duration = 0

    with open(infile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            if row['session_duration'] and row['inactive_duration']:
                total_duration += int(row['session_duration'])
                if row['inactive_status'] == "TRUE":
                    inactive_sess += 1
                    total_inactive_duration += int(row['inactive_duration'])
                total_active_duration += int(row['session_duration']) - int(row['inactive_duration'])

        print("Average session duration: ", total_duration / total_sess / 60)
        print("Average active session duration: ", total_active_duration / total_sess / 60)
        print("Average inactivity: ", total_inactive_duration / total_sess / 60,
              "\nProportion sessions with inactivity: ", inactive_sess / total_sess)


def analysis_date(infile: str):
    """days of week (Oct 1, 2019 10/1/19 was tuesday)"""
    days = dict.fromkeys(['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun'], 0)
    total_durations = dict.fromkeys(['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun'], 0)
    active_durations = dict.fromkeys(['mon', 'tues', 'wed', 'thurs', 'fri', 'sat', 'sun'], 0)
    with open(infile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['login_date']:
                date_list = row['login_date'].split("/")
                day = int(date_list[1])
                if day % 7 == 1:
                    days["tues"] += 1
                    total_durations["tues"] += int(row['session_duration'])
                    active_durations["tues"] += int(row['session_duration']) - int(row['inactive_duration'])
                elif day % 7 == 2:
                    days["wed"] += 1
                    total_durations["wed"] += int(row['session_duration'])
                    active_durations["wed"] += int(row['session_duration']) - int(row['inactive_duration'])
                elif day % 7 == 3:
                    days["thurs"] += 1
                    total_durations["thurs"] += int(row['session_duration'])
                    active_durations["thurs"] += int(row['session_duration']) - int(row['inactive_duration'])
                elif day % 7 == 4:
                    days["fri"] += 1
                    total_durations["fri"] += int(row['session_duration'])
                    active_durations["fri"] += int(row['session_duration']) - int(row['inactive_duration'])
                elif day % 7 == 5:
                    days["sat"] += 1
                    total_durations["sat"] += int(row['session_duration'])
                    active_durations["sat"] += int(row['session_duration']) - int(row['inactive_duration'])
                elif day % 7 == 6:
                    days["sun"] += 1
                    total_durations["sun"] += int(row['session_duration'])
                    active_durations["sun"] += int(row['session_duration']) - int(row['inactive_duration'])
                elif day % 7 == 0:
                    days["mon"] += 1
                    total_durations["mon"] += int(row['session_duration'])
                    active_durations["mon"] += int(row['session_duration']) - int(row['inactive_duration'])
        print(days)
        print(active_durations)
        for day in days:
            print(day, "Avg duration", total_durations[day] / days[day] / 60,
                  "\n   Avg active duration", active_durations[day] / days[day] / 60)


def user_retention(infile: str):
    """analysing returning users"""
    userlist = []
    with open(infile, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row["customer_id"]:
                userlist.append(row["customer_id"])
    # maps customer_id to log in frequency
    users = {}
    for i in userlist:
        users[i] = users.get(i, 0) + 1
    freqs = []
    for uid in users:
        freqs.append(users[uid])

    sorted_freqs = sorted(freqs)
    # maps num log in to how many logged in that many times
    freq_appears = {}
    for freq in sorted_freqs:
        freq_appears[freq] = freq_appears.get(freq, 0) + 1
    print("frequencies ", freq_appears)
    print(f"average sessions/month (total {sum(freqs)}, num users {len(freqs)})", sum(freqs) / len(freqs))


if __name__ == '__main__':
    filename = "showwcase_sessions.csv"
    analysis_basic(filename)
    session_times(filename)
    analysis_date(filename)
    user_retention(filename)
