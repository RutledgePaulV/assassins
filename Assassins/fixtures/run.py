import os
import django
from fixtures.assignments import AssignmentsFixture

from .member import *
from .site import *
from .games import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Assassins.settings")
django.setup()

print('Generating user objects.')
member_fixture = MemberFixture()
member_fixture.gen(20)

print('Generating location objects.')
location_fixture = LocationFixture()
location_fixture.gen(20)

print('Generating social media photo objects.')
social_media_fixture = SocialMediaPhotosFixture()
social_media_fixture.gen(50)

print('Generating rules objects.')
rule_set_fixture = RulesFixture()
rule_set_fixture.gen(15)

print('Generating game objects.')
game_fixture = GameFixture()
game_fixture.gen(20)

print('Generating assignments')
assignments_fixture = AssignmentsFixture()
assignments_fixture.gen(1)