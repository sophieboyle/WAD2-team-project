from django.test import TestCase
from spuni.models import Song, UserProfile
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

class SongModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Song.objects.create(name="Shiba Inus are the Best", artist="shibe1",
                            albumArt="https://66.media.tumblr.com/1c0f4fbad5ca9e7262cf4a5b5ba8db51/tumblr_oxz891R1jI1s9dacgo10_250.gifv",
                            upvotes=10)
    
    def test_slug_construction(self):
        song = Song.objects.get(id=1)
        name = song.name
        artist = song.artist
        slug = song.slug
        self.assertEquals(slug, f"{slugify(name)}-{slugify(artist)}")

    def test_name_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("name").verbose_name
        self.assertEquals(field_label, "name")
    
    def test_album_art_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("albumArt").verbose_name
        self.assertEquals(field_label, "albumArt")
    
    def test_upvotes_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("upvotes").verbose_name
        self.assertEquals(field_label, "upvotes")
    
    def test_artist_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("artist").verbose_name
        self.assertEquals(field_label, "artist")
    
    def test_slug_label(self):
        song = Song.objects.get(id=1)
        field_label = song._meta.get_field("slug").verbose_name
        self.assertEquals(field_label, "slug")
    
    def test_name_max_length(self):
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("name").max_length
        self.assertEquals(max_length, 128)
    
    def test_artist_max_length(self):
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("artist").max_length
        self.assertEquals(max_length, 128)
    
    def test_album_art_max_length(self):
        song = Song.objects.get(id=1)
        max_length = song._meta.get_field("albumArt").max_length
        self.assertEquals(max_length, 200)
    
    def test_str(self):
        song = Song.objects.get(id=1)
        self.assertEquals(str(song), song.name)

class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        u = User.objects.create_user(username="testshibe")
        u.set_password("iamtestshibe")
        u.save()
        UserProfile.objects.create(user=u,
                                    photo="https://i.kym-cdn.com/photos/images/newsfeed/001/688/970/a72.jpg")

    def test_user_label(self):
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("user").verbose_name
        self.assertEquals(user_label, "user")
    
    def test_photo_label(self):
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("photo").verbose_name
        self.assertEquals(user_label, "photo")

    def test_upvoted_songs_label(self):
        up = UserProfile.objects.get(id=1)
        user_label = up._meta.get_field("upvotedSongs").verbose_name
        self.assertEquals(user_label, "upvotedSongs")
    
    def test_photo_max_length(self):
        up = UserProfile.objects.get(id=1)
        max_length = up._meta.get_field("photo").max_length
        self.assertEquals(max_length, 200)
    