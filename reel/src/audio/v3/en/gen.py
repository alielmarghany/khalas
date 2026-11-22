import json,subprocess,sys
L={'l1':"[tired, sarcastic] 2 AM... still replying to customers?",
   'l2':"[annoyed, fast] How much? Available? Address? Same questions. Every day!",
   'l3':"[excited] Let khalas reply, and confirm orders for you.",
   'l4':"[softly, satisfied] While you sleep... orders get confirmed.",
   'l5':"[excited] Comment khalas, and I'll send you the link!"}
take=sys.argv[1]
for k in sys.argv[2:]:
    fn=f'en/{k}_{take}'
    r=subprocess.run(['curl','-s','-X','POST','https://api.elevenlabs.io/v1/text-to-speech/iP95p4xoKVk53GoZ742B?output_format=mp3_44100_128','-H','xi-api-key: x','-H','Content-Type: application/json','-d',json.dumps({'text':L[k],'model_id':'eleven_v4','language_code':'en'}),'-o',fn+'.mp3','-w','%{http_code}'],capture_output=True,text=True).stdout
    if r!='200': print(fn,r,open(fn+'.mp3').read()[:150]); continue
    subprocess.run(['ffmpeg','-v','error','-y','-i',fn+'.mp3','-af','silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse','-ar','48000',fn+'.wav'])
    t=json.loads(subprocess.run(['curl','-s','-X','POST','https://api.elevenlabs.io/v1/speech-to-text','-H','xi-api-key: x','-F','model_id=scribe_v1','-F','file=@'+fn+'.wav'],capture_output=True).stdout)
    json.dump(t,open(fn+'.stt.json','w'),ensure_ascii=False)
    d=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn+'.wav'],capture_output=True,text=True).stdout.strip()
    print(f'{fn} {d[:4]}s | {t.get("text")}')
