import os, sys, argparse

parser = argparse.ArgumentParser(
	prog='XTTS-RVC-UI',
	description='Gradio UI for XTTSv2 and RVC'
)

parser.add_argument('-s', '--silent', action=argparse.BooleanOptionalAction, default=False)
parser.add_argument('-a', '--api', action=argparse.BooleanOptionalAction, default=False)
args = parser.parse_args()

if args.silent: 
	print('Enabling silent mode.')
	sys.stdout = open(os.devnull, 'w')
	
if args.api:
	print("Starting API.")
	import api
	api.startAPI()
else:
	print("Starting app.")
	import app
	app.main()