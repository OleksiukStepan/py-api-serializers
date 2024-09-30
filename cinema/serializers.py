from rest_framework import serializers

from cinema.models import Genre, Actor, CinemaHall, Movie, MovieSession


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["id", "name"]


class ActorSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    def get_full_name(self, actor: Actor) -> str:
        return str(actor)

    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name", "full_name"]


class CinemaHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = CinemaHall
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "duration", "genres", "actors"]


class MovieListSerializer(MovieSerializer):
    genres = serializers.SerializerMethodField()
    actors = serializers.SerializerMethodField()

    def get_genres(self, movie: Movie) -> list[str]:
        return [str(genre) for genre in movie.genres.all()]

    def get_actors(self, movie: Movie) -> list[str]:
        return [str(actor) for actor in movie.actors.all()]


class MovieRetrieveSerializer(MovieSerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)


class MovieSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieSession
        fields = [
            "id",
            "show_time",
            "movie",
            "cinema_hall",
        ]


class MovieSessionListSerializer(MovieSessionSerializer):
    movie_title = serializers.CharField(source="movie.title", read_only=True)
    cinema_hall_name = serializers.CharField(
        source="cinema_hall.name", read_only=True
    )
    cinema_hall_capacity = serializers.IntegerField(
        source="cinema_hall.capacity", read_only=True
    )

    class Meta(MovieSessionSerializer.Meta):
        fields = [
            "id",
            "show_time",
            "movie_title",
            "cinema_hall_name",
            "cinema_hall_capacity"
        ]


class MovieSessionRetrieveSerializer(MovieSessionSerializer):
    movie = MovieListSerializer(read_only=True)
    cinema_hall = CinemaHallSerializer(read_only=True)

    class Meta(MovieSessionSerializer.Meta):
        fields = [
            "id",
            "show_time",
            "movie",
            "cinema_hall",
        ]
