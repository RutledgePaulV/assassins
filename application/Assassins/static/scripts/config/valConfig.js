/**
 * This module defines the configuration for bootstrap validator which
 * is used throughout the site for front-end validation of form fields.
 *
 * A small set of custom validator plugins are also being used:
 *
 *    -cleanLanguage: Fails validation if field contains profanity
 *
 *    -command: Uses a memoized and throttled server command to validate
 */
define(['jquery',

/**
 * Unreferenced MIDS
 */
	'scripts/plugins/formvalidation/clean',
	'scripts/plugins/formvalidation/command',
	'scripts/plugins/formvalidation/linked'
], function ($) {

	var BasePasswordValidators = {
		notEmpty: {
			message: 'Your password cannot be empty.'
		},
		strLength: {
			min: 8,
			max: 15,
			message: 'Your password must be between 8 and 15 characters.'
		},
		regexp: {
			regexp: /([\!|\@|\#|\$|\%]+.*[0-9]+)|([0-9]+.*[\!|\@|\#|\$|\%]+)/,
			message: 'Your password must contain at least one digit and one of: ! @ # $ %'
		}
	};


	return {
		CONTAINER: 'popover',

		ICONS: {
			valid: 'glyphicon glyphicon-ok',
			invalid: 'glyphicon glyphicon-remove',
			validating: 'glyphicon glyphicon-refresh'
		},

		FIRST_NAME: {
			validators: {
				notEmpty: {
					message: 'Your first name is required and cannot be empty.'
				},
				regexp: {
					regexp: /^[a-zA-Z]+$/,
					message: 'Your first name cannot contain anything other than alphabetic characters.'
				}
			}
		},

		LAST_NAME: {
			validators: {
				notEmpty: {
					message: 'Your last name is required and cannot be empty.'
				},
				regexp: {
					regexp: /^[a-zA-Z]+$/,
					message: 'Your last name cannot contain anything other than alphabetic characters.'
				}
			}
		},

		LOGIN_EMAIL: {
			validators: {
				notEmpty: {
					message: 'Your email cannot be empty'
				},
				emailAddress: {
					message: 'You did not enter a valid email address'
				}
			}
		},

		EMAIL: {
			validators: {
				notEmpty: {
					message: 'The email is required and cannot be empty'
				},
				emailAddress: {
					message: 'The input is not a valid email address'
				},
				command: {
					query: function (email, commands) {
						return commands.VALIDATE_EMAIL.fire({email: email});
					},
					delay: 1000,
					message: 'An account for this email already exists.'
				}
			}
		},

		PHONE: {
			validators: {
				phone: {
					country: 'US',
					message: 'Please enter a valid phone number.'
				},
				regexp: {
					regexp: /^\d{3}\-\d{3}\-\d{4}/,
					message: 'Number must match format: ###-###-####'
				},
				notEmpty: {
					enabled: false,
					message: 'The phone number cannot be empty if you want to receive texts.'
				}
			}
		},

		LOGIN_PASSWORD: {
			validators: {
				notEmpty: {
					message: 'You cannot have an empty password.'
				}
			}
		},

		CURRENT_PASSWORD: {
			validators: {
				notEmpty: {
					message: 'Your password cannot be empty.'
				},
				command: {
					query: function (password, commands) {
						return commands.VALIDATE_PASSWORD.fire({password: password});
					},
					delay: 1000,
					message: 'The provided password is incorrect.'
				}
			}
		},

		PASSWORD1: {
			validators: $.extend({}, BasePasswordValidators, {
				identical: {
					field: 'password2',
					message: 'The passwords do not match.'
				}
			})
		},

		PASSWORD2: {
			validators: $.extend({}, BasePasswordValidators, {
				identical: {
					field: 'password1',
					message: 'The passwords do not match.'
				}
			})
		},

		SLOGAN: {
			validators: {
				cleanLanguage: {
					message: 'Please, no foul language. This is a family friendly site.'
				}
				,
				regexp: {
					regexp: /([a-zA-Z])/,
					message: 'Only alphabet characters are allowed.'
				}
			}
		},

		BIOGRAPHY: {
			validators: {
				cleanLanguage: {
					message: 'Please, no foul language. This is a family friendly site.'
				}
			}
		},

		SEARCH: {
			validators: {
				notEmpty: {
					message: 'No use in searching on an empty term!'
				}
			}
		},

		GAME_TITLE: {
			validators: {
				notEmpty: {
					message: 'You must provide a title.'
				},
				cleanLanguage: {
					message: 'Please, no foul language.'
				},
				stringLength: {
					min: 3,
					max: 15,
					trim: true,
					message: 'Your title must be between 3 and 15 characters'
				}
			}
		},

		GAME_INTRO: {
			validators: {
				notEmpty: {
					message: 'You must provide an intro.'
				},
				cleanLanguage: {
					message: 'Please, no foul language.'
				},
				stringLength: {
					min: 96,
					max: 512,
					trim: true,
					message: 'Please provide a more descriptive intro.'
				}
			}
		},

		ADDRESS: {
			validators: {
				notEmpty: {
					message: 'You must provide an address.'
				},
				stringLength: {
					max: 512,
					message: 'You sure that\'ts your address? It\'s ridiculously long.'
				}
			}
		},

		CITY: {
			validators: {
				notEmpty: {
					message: 'You must provide a city.'
				},
				stringLength: {
					max: 50,
					message: 'That\'ts a really long city. Did you do something wrong?'
				}
			}
		},

		ZIP: {
			validators: {
				notEmpty: {
					message: 'You must provide a zip code.'
				},
				zipCode: {
					country: 'US',
					message: 'You did not provide a valid zip code.'
				}
			}
		},

		STATE: {
			validators: {
				notEmpty: {
					message: 'You must select a state.'
				}
			}
		},

		DATE_TIME_PICKER: {
			validators: {
				date: {
					format: 'MM/DD/YYYY h:m A',
					message: 'The value is not a valid date.'
				},
				notEmpty: {
					message: 'You must provide a date.'
				}
			}
		},

		INTEGER: {
			validators: {
				integer: {
					message: 'You must provide an integer.'
				}
			}
		}
	}
});