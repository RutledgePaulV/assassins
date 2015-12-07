REQUIRE_BASE_URL = "."
REQUIRE_ENVIRONMENT = "auto"
REQUIRE_BUILD_PROFILE = False
REQUIRE_EXCLUDE = ("build.txt",)
REQUIRE_JS = "requirejs/require.js"
REQUIRE_STANDALONE_MODULES = {}


def add_module(name):
	out_path = "{0}.js".format(name.replace('scripts/', 'dist/'))
	REQUIRE_STANDALONE_MODULES[name] = {
		'out': out_path,
		'build_profile': 'scripts/build.js',
		'insert_require': True
	}


# each of these will be optimized and shimmed with almond.js
[add_module(module) for module in (

	# main geek module
	'scripts/geek/main',

	# main game modules
	'scripts/game/shared/affix',
	'scripts/game/create/main',
	'scripts/game/search/main',
	'scripts/game/management/main',
	'scripts/game/leaderboards/main',

	# main member modules
	'scripts/member/profile/main',
	'scripts/member/auth/login/main',
	'scripts/member/register/main',
	'scripts/member/assignments/main',
)]
