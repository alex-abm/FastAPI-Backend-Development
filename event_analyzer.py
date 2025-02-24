class EventAnalyzer:
    @staticmethod
    def get_joiners_multiple_meetings_method(events):
        joiners_meetings_count = {}
        for event in events:
            joiners = event.get('joiners', [])
            for joiner in joiners:
                joiner_email = joiner.get('email')
                joiners_meetings_count[joiner_email] = joiners_meetings_count.get(joiner_email, 0) + 1

        return [joiner_email for joiner_email, count in joiners_meetings_count.items() if count >= 2]
