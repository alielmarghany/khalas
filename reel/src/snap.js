const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920},deviceScaleFactor:1});
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+__dirname+'/reel.html');await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(300);
const mode=process.argv[2];
if(mode==='all'){fs.mkdirSync('frames',{recursive:true});const N=450;const t0=Date.now();
 for(let f=0;f<N;f++){await p.evaluate(t=>render(t),f/30);await p.screenshot({path:`frames/f${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:92});}
 console.log('done',(Date.now()-t0)/1000);}
else{fs.mkdirSync('snaps',{recursive:true});for(const t of process.argv.slice(2).map(Number)){await p.evaluate(t=>render(t),t);await p.screenshot({path:`snaps/t${t.toFixed(2)}.jpg`,type:'jpeg',quality:80});}}
await b.close();})();
