







def verify_date(tournament_start, tournament_end):

    tournament_start = tournament_start.replace("/", "")
    tournament_end = tournament_end.replace("/", "")

    if re.match(r'^\d{8}$', tournament_start) or not re.match(r'^\d{8}$', tournament_end):
        return None

    try:
        tournament_start_date = datetime.strptime(tournament_start, "%d%m%Y")
        tournament_end_date = datetime.strptime(tournament_end, "%d%m%Y")

        if tournament_end_date < tournament_start_date:
            return None

        return (tournament_start_date.strftime("%d/%m/%Y"),
                tournament_end_date.strftime("%d/%m/%Y"))

    except ValueError:
        return None