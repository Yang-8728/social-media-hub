import subprocess,json,os  
d='videos/merged/ai_vanvan'  
f='tools/ffmpeg/ffprobe.exe'  
vs=sorted([x for x in os.listdir(d) if x.endswith('.mp4')])  
for v in vs:  
 p=os.path.join(d,v);r=subprocess.run([f,'-v','error','-show_entries','format=duration','-of','json',p],capture_output=True,text=True,shell=True)  
 dur=float(json.loads(r.stdout)['format']['duration']) if r.returncode==0 else 0  
 print(f'{v:30} {int(dur//60)}:{int(dur%60):02} ({int(dur)}s) {os.path.getsize(p)/1024/1024:.2f}MB')  
