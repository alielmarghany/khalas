import json,subprocess,sys
L={'l1':'[Egyptian accent][exhausted, sarcastic] الساعة اتنين بالليل… ولسه بترد على الزباين؟',
   'l2':'[Egyptian accent][annoyed, fast] بكام؟ متاح؟ العنوان فين؟ كل يوم نفس الأسئلة!',
   'l3':'[Egyptian accent][excited] خلّي خلاص يرد عليهم، ويأكد الأوردر لوحده.',
   'l4':'[Egyptian accent][softly, satisfied] وانت نايم… الأوردرات بتتأكد.',
   'l5':'[Egyptian accent][excited] اكتب خلاص في الكومنت، وهبعتلك اللينك!'}
take=sys.argv[1]
for k in sys.argv[2:]:
    fn=f'chris/{k}_{take}'
    r=subprocess.run(['curl','-s','-X','POST','https://api.elevenlabs.io/v1/text-to-speech/iP95p4xoKVk53GoZ742B?output_format=mp3_44100_128','-H','xi-api-key: x','-H','Content-Type: application/json','-d',json.dumps({'text':L[k],'model_id':'eleven_v4','language_code':'ar'}),'-o',fn+'.mp3','-w','%{http_code}'],capture_output=True,text=True).stdout
    if r!='200': print(fn,r); continue
    subprocess.run(['ffmpeg','-v','error','-y','-i',fn+'.mp3','-af','silenceremove=start_periods=1:start_threshold=-40dB,areverse,silenceremove=start_periods=1:start_threshold=-40dB,areverse','-ar','48000',fn+'.wav'])
    t=json.loads(subprocess.run(['curl','-s','-X','POST','https://api.elevenlabs.io/v1/speech-to-text','-H','xi-api-key: x','-F','model_id=scribe_v1','-F','file=@'+fn+'.wav'],capture_output=True).stdout)
    json.dump(t,open(fn+'.stt.json','w'),ensure_ascii=False)
    d=subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',fn+'.wav'],capture_output=True,text=True).stdout.strip()
    print(f'{fn} {d[:4]}s | {t.get("text")}')
