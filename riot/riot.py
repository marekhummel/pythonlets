from collections import defaultdict
import cassiopeia as cass
from pprint import pprint


SUMMONER = 'Plexian'
REGION = cass.Region.europe_west


def config():
    config = cass.get_default_config()
    key = [line.split('=')[1] for line in open('config.cfg', mode='r').readlines() if line.startswith('RIOT_KEY')][0]
    config['pipeline']['RiotAPI']['api_key'] = key
    config['logging']['print_calls'] = False
    cass.apply_settings(config)


def mastery_4(masteries: list[cass.ChampionMastery]):
    return {c.champion.name: c.points_until_next_level for c in masteries if c.level == 4}


def mastery_counts(masteries: list[cass.ChampionMastery]):
    counts = defaultdict(lambda: 0)
    for cm in masteries:
        counts[cm.level] += 1
    return dict(counts)


def mastery_tokens(masteries: list[cass.ChampionMastery]):
    tokens = [cm for cm in masteries if cm.level in [5, 6]]
    available = [c for c in tokens if c.tokens < (c.level - 3)]
    return {c.champion.name: c.tokens for c in available}


def mastery_chests(masteries: list[cass.ChampionMastery], min_level=None):
    chests_avail = [c for c in masteries if not c.chest_granted and (min_level is None or c.level >= min_level)]
    chests_avail.sort(key=lambda c: c.level, reverse=True)
    return [c.champion.name for c in chests_avail]


def mastery_unplayed(masteries: list[cass.ChampionMastery]):
    return [c.champion.name for c in masteries if c.level == 0]


config()
summoner: cass.Summoner = cass.get_summoner(name=SUMMONER, region=REGION)
champions: list[cass.ChampionMastery] = summoner.champion_masteries
# match: cass.core.spectator.CurrentGameInfoData = summoner.current_match

# r = cass.Rank
# pprint([t.to_dict() for t in match.teams])
# pprint(summoner.match_history.search("Katarina"))


# print(summoner.level)
print(summoner.name)
pprint(mastery_4(champions))
# pprint(mastery_tokens(champions))
# pprint(mastery_chests(champions, 7))
pprint(mastery_counts(champions))
pprint(mastery_unplayed(champions))
# print(summoner.to_dict())
