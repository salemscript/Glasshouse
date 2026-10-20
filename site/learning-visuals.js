/* Original, source-specific interactive illustrations. No external media or libraries. */
'use strict';
window.LearningVisuals = (() => {
  const C = { bg:'#101b25', grid:'#2b3946', ink:'#eaf1f3', muted:'#aabac3', blue:'#60d8d0', coral:'#ff7967', gold:'#ffd06e' };
  const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const num = n => Number.isFinite(n) ? Number(n.toFixed(3)) : 0;
  const clamp = (n,a,b) => Math.min(b,Math.max(a,n));
  const fmt = (n,d=2) => Number(n).toFixed(d).replace(/\.0+$/,'');
  const point = (x,y) => `${num(x)},${num(y)}`;
  const txt = (x,y,s,color=C.ink,size=18,anchor='start') => `<text x="${num(x)}" y="${num(y)}" fill="${color}" font-size="${size}" text-anchor="${anchor}">${esc(s)}</text>`;
  const line = (x1,y1,x2,y2,color=C.grid,width=1,extra='') => `<line x1="${num(x1)}" y1="${num(y1)}" x2="${num(x2)}" y2="${num(y2)}" stroke="${color}" stroke-width="${width}" ${extra}/>`;
  const dot = (x,y,color=C.blue,r=6,fill=color) => `<circle cx="${num(x)}" cy="${num(y)}" r="${r}" fill="${fill}" stroke="${color}" stroke-width="3"/>`;
  const arrow = (id,x1,y1,x2,y2,color='blue',width=3) => line(x1,y1,x2,y2,C[color],width,`marker-end="url(#lv-${id}-${color})"`);
  const plot = (xmin,xmax,ymin,ymax,x=72,y=58,w=470,h=310) => ({X:v=>x+(v-xmin)/(xmax-xmin)*w,Y:v=>y+h-(v-ymin)/(ymax-ymin)*h,x,y,w,h,xmin,xmax,ymin,ymax});
  function path(fn,from,to,p,samples=120) {
    let d='';
    for(let i=0;i<=samples;i++){const x=from+(to-from)*i/samples,y=fn(x);if(Number.isFinite(y))d+=(d?'L':'M')+point(p.X(x),p.Y(y));}
    return d;
  }
  const curve = (d,color,width=3,extra='') => `<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linejoin="round" ${extra}/>`;
  function grid(p,xTicks=[],yTicks=[],showY=true) {
    let s='';
    for(const x of xTicks)s+=line(p.X(x),p.y,p.X(x),p.y+p.h)+txt(p.X(x),p.y+p.h+24,fmt(x),C.muted,15,'middle');
    for(const y of yTicks)s+=line(p.x,p.Y(y),p.x+p.w,p.Y(y))+(showY?txt(p.x-12,p.Y(y)+5,fmt(y),C.muted,15,'end'):'');
    const y0=clamp(p.Y(0),p.y,p.y+p.h),x0=clamp(p.X(0),p.x,p.x+p.w);
    return s+line(p.x,y0,p.x+p.w,y0,C.muted,1.5)+line(x0,p.y,x0,p.y+p.h,C.muted,1.5);
  }
  function svg(id,body,description) {
    let defs='';
    for(const color of ['blue','coral','gold'])defs+=`<marker id="lv-${id}-${color}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="${C[color]}"/></marker>`;
    return `<svg viewBox="0 0 800 440" role="img" font-family="Inter,Arial,sans-serif" aria-label="${esc(description)}" xmlns="http://www.w3.org/2000/svg"><desc>${esc(description)}</desc><defs>${defs}</defs><rect width="800" height="440" fill="${C.bg}"/>${body}</svg>`;
  }
  const models = {
    'removable-limit': {
      ids:['calculus-section-2-3-11','stewart-2-3-11'], title:'Approach a missing point',
      prediction:'Predict: if one point is missing, can the nearby values still approach a height?',
      observation:'Watch the moving point from each side. Which feature determines the limit: the hole or the surrounding graph?',
      description:'The graph of (x² − 6x + 5)/(x − 5) follows a line with a hole at x = 5. A point approaches the hole from either side.',
      note:'The graph uses the exact function from this exercise. The limit’s numeric value appears after the guided solution is completed.',
      parameter:{key:'gap',label:'Starting distance from x = 5',min:.05,max:2,step:.05,value:1,unit:''}, sides:true, duration:6500,
      frame(u,p,reveal){
        const map=plot(2,8,0,8),gap=p.gap*Math.exp(-4*u),x=5+p.side*gap,y=x-1;
        let body=grid(map,[2,3,4,5,6,7,8],[0,2,4,6,8],false)+curve(path(v=>v-1,2,8,map),C.blue,4);
        body+=line(map.X(5),map.y,map.X(5),map.y+map.h,C.gold,1,'stroke-dasharray="5 6"');
        body+=dot(map.X(5),map.Y(4),C.gold,8,C.bg)+dot(map.X(x),map.Y(y),C.coral);
        body+=txt(map.X(x)+12,map.Y(y)-12,'(x, f(x))',C.coral,17)+txt(map.X(5)+12,map.Y(4)+30,'missing point',C.gold,16);
        body+=txt(570,94,'Same neighboring graph',C.blue,18)+txt(570,130,'x² − 6x + 5',C.ink,23)+line(570,143,748,143,C.ink,1.5)+txt(655,172,'x − 5',C.ink,23,'middle');
        body+=txt(570,230,'x → 5',C.gold,24)+txt(570,267,'f(x) → ?',C.coral,24)+txt(570,316,'The point itself',C.muted,16)+txt(570,340,'need not exist.',C.muted,16);
        return {svg:svg('limit',body,this.description),readouts:[['Approach',p.side<0?'From the left':'From the right'],['Moving x',fmt(x,4)],['Limit',reveal?'4':'Complete the guided steps']],values:{x,y,gap}};
      }
    },
    'secant-slope': {
      ids:['calculus-section-2-3-18','stewart-2-3-18'],title:'A secant becomes a tangent',
      prediction:'Predict: as h shrinks, what happens to the two points and the secant line?',
      observation:'The horizontal and vertical changes shrink together. The quotient describes a slope, even while each change approaches zero.',
      description:'A point on y = x³ moves toward (2,8). The horizontal change h and vertical change (2+h)³−8 form a secant triangle.',
      note:'The highlighted quotient is the exact expression in the problem. At h = 0 the original quotient is undefined; the tangent shows its limiting geometry.',
      parameter:{key:'h',label:'Horizontal change h',min:-1,max:1,step:.01,value:1,unit:''},duration:6500,
      frame(u,p,reveal){
        const h=p.h*Math.exp(-4*u),x=2+h,y=x*x*x,map=plot(1,3.05,0,29),m=12+6*h+h*h;
        let body=grid(map,[1,1.5,2,2.5,3],[0,8,16,24])+curve(path(v=>v*v*v,1,3,map),C.blue,4);
        body+=curve(path(v=>8+m*(v-2),1.5,2.9,map),C.gold,2,'stroke-dasharray="7 5"');
        body+=line(map.X(2),map.Y(8),map.X(x),map.Y(8),C.gold,3)+line(map.X(x),map.Y(8),map.X(x),map.Y(y),C.coral,3);
        body+=dot(map.X(2),map.Y(8))+dot(map.X(x),map.Y(y),C.coral)+txt(map.X(2)-10,map.Y(8)+31,'(2, 8)',C.blue,16,'end');
        if(Math.abs(h)>.13)body+=txt((map.X(2)+map.X(x))/2,map.Y(8)+23,'h',C.gold,18,'middle')+txt(map.X(x)+12,(map.Y(8)+map.Y(y))/2,'Δy',C.coral,18);
        body+=txt(570,100,'The slope is a ratio',C.gold,18)+txt(570,146,'(2 + h)³ − 8',C.coral,22)+line(570,158,751,158,C.ink,1.5)+txt(660,186,'h',C.gold,23,'middle');
        body+=txt(570,246,'h → 0',C.gold,24)+txt(570,282,'secant → tangent',C.blue,18)+txt(570,334,'y = x³',C.blue,22);
        return {svg:svg('secant',body,this.description),readouts:[['Horizontal change',fmt(h,4)],['At h = 0',h===0?'Original quotient undefined':'Two distinct points'],['Limiting slope',reveal?'12':'Complete the guided steps']],values:{h,x,y,slope:m}};
      }
    },
    'sliding-ladder': {
      ids:['calculus-section-3-9-33','stewart-3-9-33'],title:'Two motions, one constraint',
      prediction:'Predict: if the bottom moves away at a steady rate, must the top also move at a steady rate?',
      observation:'The triangle changes while the ladder keeps its length. Relate the two rates at the instant given in the problem.',
      description:'A rigid ladder rests on a vertical wall and horizontal floor. Its bottom slides away, its top slides downward, and the right triangle retains a fixed hypotenuse.',
      note:'At x = 3 m the given rates are x′ = 0.20 m/s and y′ = −0.15 m/s. This illustration keeps x′ constant; y′ changes afterward. Geometry is schematic, not a ruler.',
      parameter:{key:'x',label:'Explore a starting bottom position',min:1.8,max:4.5,step:.05,value:3,unit:'m'},duration:6500,
      frame(u,p,reveal){
        const interval=Math.min(4,(4.85-p.x)/.2),t=u*interval,x=p.x+.2*t,y=Math.sqrt(25-x*x),dy=-x*.2/y;
        const bx=145+x*62,ty=355-y*62;
        let body=line(145,42,145,356,C.muted,7)+line(145,355,530,355,C.muted,7);
        for(let y0=62;y0<355;y0+=28)body+=line(124,y0,142,y0-17,C.grid,2);
        body+=`<polygon points="145,355 ${point(bx,355)} ${point(145,ty)}" fill="${C.blue}" opacity=".06"/>`;
        body+=line(145,ty,bx,355,C.gold,10)+line(145,ty,bx,355,C.bg,3);
        for(let f=.13;f<1;f+=.13){const xx=145+(bx-145)*f,yy=ty+(355-ty)*f;body+=line(xx-10,yy+7,xx+10,yy-7,C.gold,3);}
        body+=dot(145,ty,C.coral)+dot(bx,355,C.blue)+arrow('ladder',bx,391,bx+57,391,'blue')+arrow('ladder',101,ty,101,ty+58,'coral');
        body+=txt((145+bx)/2,336,'x',C.blue,25,'middle')+txt(165,(355+ty)/2,'y',C.coral,25)+txt((145+bx)/2+35,(355+ty)/2-15,'L (constant)',C.gold,18);
        body+=txt(577,96,'x² + y² = L²',C.ink,23)+txt(577,150,'x x′ + y y′ = 0',C.ink,21)+txt(577,227,'Given at x = 3 m',C.muted,17)+txt(577,262,'x′ = +0.20 m/s',C.blue,18)+txt(577,293,'y′ = −0.15 m/s',C.coral,18);
        return {svg:svg('ladder',body,this.description),readouts:[['Bottom position',fmt(x,2)+' m'],['Elapsed model time',fmt(t,2)+' s'],['Ladder length',reveal?'5 m':'Complete the guided steps']],values:{x,y,t,dx:.2,dy,lengthSquared:x*x+y*y}};
      }
    },
    'between-curves': {
      ids:['calculus-section-6-1-13','stewart-6-1-13-area-portion'],title:'Build an area from thin strips',
      prediction:'Predict: which curve supplies the top of a vertical strip, and which supplies the bottom?',
      observation:'Each strip contributes height × width. Increasing the strip count improves the approximation; the integral captures the limit.',
      description:'The region between y = 12−x² and y = x²−6 is filled with vertical midpoint rectangles. The selected strip moves across the enclosed region.',
      note:'The exact source curves stay fixed. The strip-count slider changes the approximation, not the textbook exercise.',
      parameter:{key:'n',label:'Number of midpoint strips',min:4,max:48,step:2,value:12,unit:''},duration:7000,
      frame(u,p,reveal){
        const map=plot(-3.8,3.8,-8,15),n=Math.round(p.n),dx=6/n,index=Math.min(n-1,Math.floor(u*n)),x=-3+(index+.5)*dx,upper=12-x*x,lower=x*x-6;
        let body=grid(map,[-3,-2,-1,0,1,2,3],[-6,0,6,12]);let total=0;
        for(let i=0;i<n;i++){const xx=-3+(i+.5)*dx,top=12-xx*xx,bottom=xx*xx-6,height=top-bottom;total+=height*dx;body+=`<rect x="${num(map.X(xx-dx/2))}" y="${num(map.Y(top))}" width="${num(map.X(dx)-map.X(0))}" height="${num(map.Y(bottom)-map.Y(top))}" fill="${i===index?C.gold:C.blue}" opacity="${i===index?'.4':'.13'}" stroke="${i===index?C.gold:C.blue}" stroke-width="${i===index?2:.6}"/>`;}
        body+=curve(path(v=>12-v*v,-3.6,3.6,map),C.blue,3)+curve(path(v=>v*v-6,-3.6,3.6,map),C.coral,3);
        body+=line(map.X(x),map.Y(upper),map.X(x),map.Y(lower),C.gold,3)+dot(map.X(-3),map.Y(3),C.ink,4)+dot(map.X(3),map.Y(3),C.ink,4);
        body+=txt(565,83,'Upper: 12 − x²',C.blue,20)+txt(565,118,'Lower: x² − 6',C.coral,20)+txt(565,173,'height = upper − lower',C.gold,18)+txt(565,211,'strip area ≈ height · Δx',C.ink,17)+txt(565,272,'sum of thin strips',C.muted,18)+txt(565,306,'→ definite integral',C.ink,19);
        return {svg:svg('area',body,this.description),readouts:[['Selected strip',`${index+1} / ${n}`],['Strip width Δx',fmt(dx,3)],['Enclosed area',reveal?'72 square units':'Complete the guided steps']],values:{x,upper,lower,width:dx,midpointArea:total}};
      }
    },
    'constant-speed': {
      ids:['physics-chapter-02-problems-1','halliday10-003'],title:'Distance is an area under velocity',
      prediction:'Predict: during a sneeze, does a constant-speed car keep moving while your eyes are closed?',
      observation:'The car’s displacement and the shaded area grow together. Match seconds with a speed measured per second.',
      description:'A car moves at the fixed source speed, 90 km/h, during a 0.50 second interval. A velocity-time rectangle grows in sync with the car.',
      note:'An ideal constant-speed model of the source question. The playback is slowed for observation; its time readout uses the actual 0.50 s interval.',
      duration:6500,
      frame(u,p,reveal){
        const t=.5*u,v=25,d=v*t,carX=110+u*400,map=plot(0,.5,0,30,83,242,445,128);
        let body=line(76,185,559,185,C.muted,3);for(let x=100;x<559;x+=45)body+=line(x,202,x+23,202,C.grid,2);
        for(let i=0;i<5;i++)body+=dot(110+i*100,185,C.grid,3);
        body+=`<g transform="translate(${num(carX)},150)"><path d="M-32 8 L-24 -12 L13 -12 L28 8 L38 12 L38 28 L-38 28 L-38 13 Z" fill="${C.blue}"/><path d="M-16 -8 L9 -8 L19 7 L-23 7 Z" fill="${C.bg}"/><circle cx="-23" cy="29" r="9" fill="${C.bg}" stroke="${C.muted}" stroke-width="3"/><circle cx="23" cy="29" r="9" fill="${C.bg}" stroke="${C.muted}" stroke-width="3"/></g>`;
        body+=arrow('car',carX-19,117,carX+37,117,'blue')+txt(84,76,'v = 90 km/h',C.blue,24)+txt(84,107,'Δt = 0.50 s',C.coral,19);
        body+=grid(map,[0,.1,.2,.3,.4,.5],[0,25])+`<rect x="${map.X(0)}" y="${map.Y(v)}" width="${num(map.X(t)-map.X(0))}" height="${num(map.Y(0)-map.Y(v))}" fill="${C.gold}" opacity=".2"/>`;
        body+=line(map.X(0),map.Y(v),map.X(.5),map.Y(v),C.blue,3)+line(map.X(t),map.Y(0),map.X(t),map.Y(v),C.coral,2)+txt(83,224,'Velocity (m/s)',C.muted,16)+txt(537,428,'Time (s)',C.muted,16,'end');
        body+=txt(586,254,'distance = v · t',C.gold,23)+txt(586,304,'rectangle area',C.gold,18)+txt(586,337,'tracks displacement',C.muted,17);
        return {svg:svg('car',body,this.description),readouts:[['Source speed','90 km/h'],['Model time',fmt(t,3)+' s'],['Full-interval distance',reveal?'12.5 m ≈ 13 m (2 significant figures)':'Complete the guided steps']],values:{time:t,speed:v,distance:d}};
      }
    },
    'vector-forces': {
      ids:['physics-chapter-05-problems-1','halliday10-006'],title:'Add directions before magnitudes',
      prediction:'Predict: can forces of 9 N and 8 N be added as 17 N when they point in different directions?',
      observation:'Move the second vector to the tip of the first. The start-to-finish vector supplies the direction of acceleration.',
      description:'An eastward 9 N force and an 8 N force directed 62 degrees north of west are added head to tail. A resultant vector appears after the construction.',
      note:'The exact source forces and 3.0 kg mass stay fixed. Run animates a vector-addition construction, not the body’s trajectory.',
      duration:7000,
      frame(u,p,reveal){
        const angle=62*Math.PI/180,fx=9-8*Math.cos(angle),fy=8*Math.sin(angle),F=Math.hypot(fx,fy),origin={x:212,y:313},scale=23;
        const first={x:origin.x+9*scale,y:origin.y},second={x:-8*Math.cos(angle)*scale,y:-8*Math.sin(angle)*scale},shift=clamp(u*2,0,1),start={x:origin.x+9*scale*shift,y:origin.y},finish={x:start.x+second.x,y:start.y+second.y},netDraw=clamp((u-.5)*2,0,1);
        let body=line(82,origin.y,545,origin.y,C.grid,2)+line(origin.x,50,origin.x,378,C.grid,2)+txt(526,343,'East / +x',C.muted,16,'end')+txt(227,68,'North / +y',C.muted,16);
        body+=arrow('force',origin.x,origin.y,first.x,first.y,'blue',5)+arrow('force',start.x,start.y,finish.x,finish.y,'coral',5);
        body+=txt(318,346,'9.0 N',C.blue,21)+txt(finish.x-4,finish.y-20,'8.0 N',C.coral,21,'middle');
        if(shift<.04){const r=58,a1=Math.PI,a2=Math.PI-angle;body+=`<path d="M ${point(origin.x+r*Math.cos(a1),origin.y-r*Math.sin(a1))} A ${r} ${r} 0 0 1 ${point(origin.x+r*Math.cos(a2),origin.y-r*Math.sin(a2))}" fill="none" stroke="${C.coral}" stroke-width="2"/>`+txt(133,272,'62°',C.coral,17);}
        if(netDraw>0)body+=arrow('force',origin.x,origin.y,origin.x+fx*scale*netDraw,origin.y-fy*scale*netDraw,'gold',4)+txt(310,173,'Fnet',C.gold,20);
        body+=dot(origin.x,origin.y,C.ink,5)+txt(85,404,'Translate vectors without changing their lengths or directions.',C.muted,16);
        body+=txt(575,96,'m = 3.0 kg',C.ink,23)+txt(575,154,'Fx = 9 − 8 cos 62°',C.blue,17)+txt(575,192,'Fy = 8 sin 62°',C.coral,17)+txt(575,254,'|Fnet| = √(Fx² + Fy²)',C.gold,17)+txt(575,298,'a = |Fnet| / m',C.ink,21);
        return {svg:svg('force',body,this.description),readouts:[['Construction',u<.5?'Translate the second force':'Join the start to the finish'],['Mass','3.0 kg'],['Acceleration',reveal?'2.93 m/s² ≈ 2.9 m/s²':'Complete the guided steps']],values:{fx,fy,force:F,acceleration:F/3,translation:shift,resultantProgress:netDraw}};
      }
    },
    'acid-log-scale': {
      ids:['organic-2-16'],title:'One pKₐ step, tenfold change',
      prediction:'Predict: when pKₐ increases by one, does Kₐ get larger or smaller?',
      observation:'Equal horizontal steps change Kₐ by factors of ten. A logarithmic axis turns that exponential relationship into a line.',
      description:'The relationship Kₐ = 10 to the power of negative pKₐ is plotted with a logarithmic Kₐ axis. The HCN source value pKₐ = 9.31 is marked.',
      note:'The source asks about HCN at pKₐ = 9.31. Moving the slider explores other pKₐ values; it does not change the required source answer.',
      parameter:{key:'pka',label:'Explore pKₐ',min:1,max:14,step:.01,value:9.31,unit:''},duration:6500,
      frame(u,p,reveal){
        const map=plot(0,14,-14,0),pk=p.pka,ka=Math.pow(10,-pk),source=9.31;
        let body='';for(const k of [0,2,4,6,8,10,12,14])body+=line(map.X(k),map.y,map.X(k),map.y+map.h)+txt(map.X(k),map.y+map.h+25,k,C.muted,15,'middle');
        for(const k of [0,-5,-10,-14])body+=line(map.x,map.Y(k),map.x+map.w,map.Y(k))+txt(map.x-12,map.Y(k)+5,'10'+({'0':'⁰','-5':'⁻⁵','-10':'⁻¹⁰','-14':'⁻¹⁴'}[String(k)]),C.muted,15,'end');
        body+=curve(path(v=>-v,0,14,map),C.blue,3)+line(map.X(pk),map.Y(-pk),map.X(pk),map.y+map.h,C.coral,2,'stroke-dasharray="5 5"')+line(map.x,map.Y(-pk),map.X(pk),map.Y(-pk),C.coral,2,'stroke-dasharray="5 5"');
        body+=dot(map.X(source),map.Y(-source),C.gold,8,C.bg)+dot(map.X(pk),map.Y(-pk),C.coral)+txt(map.X(source)-12,map.Y(-source)-15,'HCN',C.gold,17,'end');
        const step=clamp(u,0,1),pk2=clamp(pk+step,0,14);body+=arrow('acid',map.X(pk),map.Y(-pk),map.X(pk2),map.Y(-pk2),'gold',3);
        body+=txt(570,423,'pKₐ',C.muted,19,'end')+txt(78,36,'Kₐ (log scale)',C.muted,18)+txt(585,98,'pKₐ = −log₁₀(Kₐ)',C.ink,19)+txt(585,147,'Kₐ = 10^(−pKₐ)',C.blue,21)+txt(585,229,'pKₐ + 1',C.gold,23)+txt(585,267,'Kₐ ÷ 10',C.coral,23);
        return {svg:svg('acid',body,this.description),readouts:[['Source HCN pKₐ','9.31'],['Exploration pKₐ',fmt(pk,2)],['Source HCN Kₐ',reveal?'4.90 × 10⁻¹⁰':'Complete the guided steps']],values:{pka:pk,ka,sourceKa:Math.pow(10,-source),comparisonPka:pk2}};
      }
    },
    'nmr-field': {
      ids:['organic-13-5','mcmurry-13-5a','mcmurry-13-5c'],title:'Same ppm, different hertz',
      prediction:'Predict: when the instrument frequency increases, which stays fixed: ppm position or separation in hertz?',
      observation:'The upper peak stays at 2.1 ppm. The lower peak moves in hertz because the instrument frequency sets the scale.',
      description:'An acetone singlet stays at 2.1 ppm while its frequency separation in hertz changes with the NMR instrument frequency.',
      note:'The source compares 200 and 500 MHz instruments. This is an axis comparison, not a simulation of spin dynamics. Intermediate frequencies are exploration.',
      parameter:{key:'mhz',label:'Explore instrument frequency',min:200,max:500,step:10,value:200,unit:'MHz'},duration:6500,
      frame(u,p,reveal){
        const MHz=p.mhz+(500-p.mhz)*u,delta=2.1,hz=delta*MHz,x0=80,x1=537,ppmX=v=>x1-v/4*(x1-x0),hzX=v=>x1-v/1400*(x1-x0);
        let body=txt(83,39,'Chemical-shift axis (ppm)',C.blue,20)+txt(83,226,'Frequency difference axis (Hz)',C.coral,20);
        const peak=(x,y,color)=>curve(`M ${point(x0,y)} L ${point(x-10,y)} C ${point(x-5,y)} ${point(x-5,y-97)} ${point(x,y-105)} C ${point(x+5,y-97)} ${point(x+5,y)} ${point(x+10,y)} L ${point(x1,y)}`,color,3);
        body+=line(x0,183,x1,183,C.muted,1.5)+peak(ppmX(delta),183,C.blue)+line(x0,366,x1,366,C.muted,1.5)+peak(hzX(hz),366,C.coral);
        for(const tick of [0,1,2,3,4])body+=line(ppmX(tick),183,ppmX(tick),190,C.muted,1)+txt(ppmX(tick),213,tick,C.muted,16,'middle');
        for(const tick of [0,400,800,1200])body+=line(hzX(tick),366,hzX(tick),373,C.muted,1)+txt(hzX(tick),398,tick,C.muted,16,'middle');
        body+=txt(ppmX(delta),72,'2.1 ppm',C.blue,18,'middle')+txt(hzX(hz),255,reveal?fmt(hz,0)+' Hz':'Δν changes',C.coral,18,'middle')+txt(550,174,'TMS',C.muted,16)+txt(550,362,'TMS',C.muted,16);
        body+=txt(598,94,'δ stays fixed',C.blue,21)+txt(598,148,'Δν = δ · MHz',C.coral,22)+txt(598,236,'Stronger field:',C.muted,18)+txt(598,272,'larger Hz gap',C.gold,20);
        return {svg:svg('nmr',body,this.description),readouts:[['Model instrument',fmt(MHz,0)+' MHz'],['Chemical shift','2.1 ppm'],['Source 200 / 500 MHz',reveal?'420 Hz / 1050 Hz':'Complete all guided parts']],values:{frequency:MHz,delta,hz}};
      }
    }
  };
  const byQuestion = Object.fromEntries(Object.entries(models).flatMap(([model,m])=>m.ids.map(id=>[id,model])));
  let active=null,animation=null,lastTime=null;
  const reduced = () => typeof matchMedia==='function' && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function defaults(model){return model.parameter?{[model.parameter.key]:model.parameter.value,side:1}:{side:1};}
  function has(id){return Boolean(byQuestion[id]||models[id]);}
  function modelId(id){return byQuestion[id]|| (models[id]?id:null);}
  function html(id){
    const mid=modelId(id),m=models[mid];if(!m)return '';
    const param=m.parameter;
    return `<section class="learning-visual" data-learning-model="${esc(mid)}" data-learning-question="${esc(id)}" aria-label="Interactive illustration"><div class="learning-heading"><span class="learning-eyebrow">SEE THE IDEA</span><h3>${esc(m.title)}</h3></div><p class="learning-prediction">${esc(m.prediction)}</p><div class="learning-stage" id="learning-stage">${m.frame(0,defaults(m),false).svg}</div><div class="learning-controls"><div class="learning-playback"><button class="btn" id="learning-run" aria-pressed="false">${reduced()?'Advance frame':'Run ▶'}</button><button class="btn light" id="learning-reset">Reset ↺</button><label class="learning-scrub-label" for="learning-scrub">Construction progress</label><input type="range" id="learning-scrub" min="0" max="1000" step="1" value="0" aria-label="Construction progress" aria-valuetext="0 percent"></div>${param?`<div class="learning-parameter"><label for="learning-parameter">${esc(param.label)} <output id="learning-parameter-value">${esc(param.value)} ${esc(param.unit)}</output></label><input type="range" id="learning-parameter" min="${param.min}" max="${param.max}" step="${param.step}" value="${param.value}"></div>`:''}${m.sides?'<div class="learning-side"><span>Approach from</span><button class="btn light" data-learning-side="-1" aria-pressed="false">Left</button><button class="btn light" data-learning-side="1" aria-pressed="true">Right</button></div>':''}</div><div class="learning-readouts" id="learning-readouts" aria-live="off"></div><p class="learning-observation">${esc(m.observation)}</p><p class="learning-note">${esc(m.note)}${reduced()?' Reduced motion is enabled: Run advances one frame at a time.':''}</p></section>`;
  }
  function paint(){
    if(!active)return;
    const m=models[active.model],f=m.frame(active.progress,active.params,active.reveal),stage=document.querySelector('#learning-stage');if(!stage)return;
    stage.innerHTML=f.svg;
    const readouts=document.querySelector('#learning-readouts');if(readouts)readouts.innerHTML=f.readouts.map(([label,value])=>`<div><span>${esc(label)}</span><b>${esc(value)}</b></div>`).join('');
    const scrub=document.querySelector('#learning-scrub');if(scrub){scrub.value=String(Math.round(active.progress*1000));scrub.setAttribute('aria-valuetext',`${Math.round(active.progress*100)} percent`);}
    const run=document.querySelector('#learning-run');if(run){run.textContent=reduced()?'Advance frame':active.running?'Pause Ⅱ':active.progress>=1?'Run again ▶':'Run ▶';run.setAttribute('aria-pressed',String(active.running));}
    if(m.parameter){const input=document.querySelector('#learning-parameter'),out=document.querySelector('#learning-parameter-value');if(input)input.value=String(active.params[m.parameter.key]);if(out)out.textContent=fmt(active.params[m.parameter.key],m.parameter.step<1?2:0)+' '+m.parameter.unit;}
    for(const side of [-1,1]){const el=document.querySelector(`[data-learning-side="${side}"]`);if(el)el.setAttribute('aria-pressed',String(active.params.side===side));}
  }
  function stop(){if(animation!==null){cancelAnimationFrame(animation);animation=null;}if(active)active.running=false;lastTime=null;}
  function unmount(){stop();active=null;}
  function mount(id){unmount();const mid=modelId(id);if(!mid)return false;const node=document.querySelector('.learning-visual');if(!node||node.dataset.learningQuestion!==String(id))return false;active={question:id,model:mid,progress:0,params:defaults(models[mid]),reveal:false,running:false};paint();return true;}
  function setReveal(reveal){if(active){active.reveal=Boolean(reveal);paint();}}
  function tick(time){
    animation=null;if(!active?.running)return;
    const delta=lastTime===null?0:Math.min(150,Math.max(0,time-lastTime));lastTime=time;
    active.progress=clamp(active.progress+delta/models[active.model].duration,0,1);
    if(active.progress>=1){active.running=false;lastTime=null;}paint();
    if(active?.running)animation=requestAnimationFrame(tick);
  }
  function run(){
    if(!active)return;
    if(reduced()){stop();active.progress=active.progress>=1?0:Math.min(1,active.progress+.25);paint();return;}
    if(active.running){stop();paint();return;}
    if(active.progress>=1)active.progress=0;
    active.running=true;lastTime=null;animation=requestAnimationFrame(tick);paint();
  }
  function reset(){if(!active)return;stop();active.progress=0;active.params=defaults(models[active.model]);paint();}
  document.addEventListener('click',e=>{const b=e.target.closest('button');if(!b||!active)return;if(b.id==='learning-run')run();else if(b.id==='learning-reset')reset();else if(b.dataset.learningSide){stop();active.params.side=Number(b.dataset.learningSide);active.progress=0;paint();}});
  document.addEventListener('input',e=>{if(!active)return;if(e.target.id==='learning-scrub'){stop();active.progress=clamp(Number(e.target.value)/1000,0,1);paint();}else if(e.target.id==='learning-parameter'){const p=models[active.model].parameter;if(!p)return;stop();active.params[p.key]=clamp(Number(e.target.value),p.min,p.max);active.progress=0;paint();}});
  document.addEventListener('visibilitychange',()=>{if(document.hidden&&active?.running){stop();paint();}});
  return {has,html,mount,unmount,setReveal,modelId,state:()=>active?JSON.parse(JSON.stringify(active)):null,
    describe:id=>{const mid=modelId(id),m=models[mid];return m?{id:mid,questionIds:[...m.ids],title:m.title,description:m.description}:null;},
    frame:(id,progress,params={},reveal=false)=>{const m=models[modelId(id)];return m?m.frame(clamp(Number(progress)||0,0,1),{...defaults(m),...params},Boolean(reveal)):null;}};
})();
