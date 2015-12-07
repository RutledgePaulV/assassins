from django.apps import AppConfig


class SiteAppConfig(AppConfig):
	name = 'Site'

	STATES = (
		('ALABAMA', 'Alabama'),
		('ALASKA', 'Alaska'),
		('ARIZONA', 'Arizona'),
		('ARKANSAS', 'Arkansas'),
		('CALIFORNIA', 'California'),
		('COLORADO', 'Colorado'),
		('CONNECTICUT', 'Connecticut'),
		('DELAWARE', 'Delaware'),
		('FLORIDA', 'Florida'),
		('GEORGIA', 'Georgia'),
		('HAWAII', 'Hawaii'),
		('IDAHO', 'Idaho'),
		('ILLINOIS', 'Illinois'),
		('INDIANA', 'Indiana'),
		('IOWA', 'Iowa'),
		('KANSAS', 'Kansas'),
		('KENTUCKY', 'Kentucky'),
		('LOUISIANA', 'Louisiana'),
		('MAINE', 'Maine'),
		('MARYLAND', 'Maryland'),
		('MASSACHUSETTS', 'Massachusetts'),
		('MICHIGAN', 'Michigan'),
		('MINNESOTA', 'Minnesota'),
		('MISSISSIPPI', 'Mississippi'),
		('MISSOURI', 'Missouri'),
		('MONTANA', 'Montana'),
		('NEBRASKA', 'Nebraska'),
		('NEVADA', 'Nevada'),
		('NEW HAMPSHIRE', 'New Hampshire'),
		('NEW JERSEY', 'New Jersey'),
		('NEW MEXICO', 'New Mexico'),
		('NEW YORK', 'New York'),
		('NORTH CAROLINA', 'North Carolina'),
		('NORTH DAKOTA', 'North Dakota'),
		('OHIO', 'Ohio'),
		('OKLAHOMA', 'Oklahoma'),
		('OREGON', 'Oregon'),
		('PENNSYLVANIA', 'Pennsylvania'),
		('RHODE ISLAND', 'Rhode Island'),
		('SOUTH CAROLINA', 'South Carolina'),
		('SOUTH DAKOTA', 'South Dakota'),
		('TENNESSEE', 'Tennessee'),
		('TEXAS', 'Texas'),
		('UTAH', 'Utah'),
		('VERMONT', 'Vermont'),
		('VIRGINIA', 'Virginia'),
		('WASHINGTON', 'Washington'),
		('WEST VIRGINIA', 'West Virginia'),
		('WISCONSIN', 'Wisconsin'),
		('WYOMING', 'Wyoming')
	)

	STATE_ABBREVIATIONS = [x[0] for x in STATES]