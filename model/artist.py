from dataclasses import dataclass, field


@dataclass
class Artist:
    ArtistId: int
    Name: str
    Tracks: list = field(default_factory=list)
    Playlists: set = field(default_factory=set)

    def __hash__(self):
        return hash(self.ArtistId)

    def __eq__(self, other):
        return self.ArtistId == other.ArtistId

    def __str__(self):
        return f"{self.Name}"
