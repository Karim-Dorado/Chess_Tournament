from utils.router import router
from controllers.controllers import main, players, tournaments, create_player, update_player_rank, list_players, \
    list_tournaments, create_tournament, start_tournament


if __name__ == '__main__':
    router.add_route("/", main)
    router.add_route("/players", players)
    router.add_route("/tournaments", tournaments)
    router.add_route("/players/create", create_player)
    router.add_route("/players/update", update_player_rank)
    router.add_route("/players/list", list_players)
    router.add_route("/tournaments/create", create_tournament)
    router.add_route("/tournaments/list", list_tournaments)
    router.add_route("/tournaments/start", start_tournament)
    router.add_route("/quit", quit)
    router.navigate("/")
