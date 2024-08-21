import gradio as gr
import core_tts

def main():
	core_tts.get_rvc_voices()
	with gr.Blocks(title='TTS RVC UI') as interface:
		with gr.Row():
			gr.Markdown("""
				#XTTS RVC UI
			""")
		with gr.Row(): 
			with gr.Column():
				lang_dropdown = gr.Dropdown(choices=core_tts.langs, value=core_tts.langs[0], label='Language')
				rvc_dropdown = gr.Dropdown(choices=core_tts.rvcs, value=core_tts.rvcs[0] if len(core_tts.rvcs) > 0 else '', label='RVC model') 
				voice_dropdown = gr.Dropdown(choices=core_tts.voices, value=core_tts.voices[0] if len(core_tts.voices) > 0 else '', label='Voice sample')
				refresh_button = gr.Button(value='Refresh')
				text_input = gr.Textbox(placeholder="Write here...")
				submit_button = gr.Button(value='Submit')
				with gr.Row():
					pitch_slider = gr.Slider(minimum=-12, maximum=12, value=0, step=1, label="Pitch")
					index_rate_slider = gr.Slider(minimum=0, maximum=1, value=0.75, step=0.05, label="Index Rate")
			with gr.Column():        
				audio_output = gr.Audio(label="TTS result", type="filepath", interactive=False)
				rvc_audio_output = gr.Audio(label="RVC result", type="filepath", interactive=False)

		submit_button.click(inputs=[rvc_dropdown, voice_dropdown, text_input, pitch_slider, index_rate_slider, lang_dropdown], outputs=[audio_output, rvc_audio_output], fn=core_tts.runtts)
		def refresh_dropdowns():
			core_tts.get_rvc_voices()
			print('Refreshed voice and RVC list!')
			return [gr.update(choices=core_tts.rvcs, value=core_tts.rvcs[0] if len(core_tts.rvcs) > 0 else ''),  gr.update(choices=core_tts.voices, value=core_tts.voices[0] if len(core_tts.voices) > 0 else '')] 

		refresh_button.click(fn=refresh_dropdowns, outputs=[rvc_dropdown, voice_dropdown])

	interface.launch(server_name="0.0.0.0", server_port=5000, quiet=True)
