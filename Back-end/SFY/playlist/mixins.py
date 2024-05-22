from song.models import SongGenres

class GenreSetMixin:    
    def set_major_genre(self, songs_relation_name):
        song_genres = SongGenres.objects.filter(**{f'song__{songs_relation_name}': self})
        genre_priority = {}

        for song_genre in song_genres:
            genre = song_genre.genre
            priority = song_genre.priority
            if genre not in genre_priority:
                genre_priority[genre] = 0
            genre_priority[genre] += self.invert_priority(priority)

        if genre_priority:
            major_genre = max(genre_priority, key=genre_priority.get)
            setattr(self, 'major_genre', major_genre)
            self.save()

    def invert_priority(self, priority):
        return 6 - priority