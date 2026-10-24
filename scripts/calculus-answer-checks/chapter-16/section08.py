from common import *
row=lambda k,*fs,**kw:A.row(8,k,*fs,**kw)
row(1,c('Why equal','Both surfaces have the same oriented boundary circle, so Stokes gives the same circulation','Both surfaces have equal area','Curl vanishes for every vector field'),limited=True)
F9=[x*y,y*z,z*x];val9=seg(F9,[0,0,1],[1,0,0])+line(F9,[s.cos(t),s.sin(t),0],0,pi/2)+seg(F9,[0,1,0],[0,0,1])
F17=[z*z,2*x*y,4*y*y];pts=[[0,0,0],[1,0,0],[1,2,1],[0,2,1],[0,0,0]]
vals={2:0,3:16*pi,4:0,5:0,6:0,7:-1,8:R(1,24),9:val9,10:pi,11:81*pi/2,12:pi,13:-32*pi,14:8*pi,15:-pi,17:sum(seg(F17,p,q) for p,q in zip(pts,pts[1:])),18:line([y+s.sin(x),z*z+s.cos(y),x**3],[s.sin(t),s.cos(t),s.sin(2*t)],0,2*pi)}
for k,val in vals.items():
 fs=[n('Curl surface integral',val),n('Boundary line integral',val)] if k in(13,14,15) else [n('Integral / work',val)]
 if k in(11,12):
  fs.append(c('b · Spanning surface','Plane disk z=1−x−y over x²+y²≤9' if k==11 else 'Saddle patch z=y²−x² over x²+y²≤1','Horizontal disk z=0 with the same3D boundary','Entire unbounded plane'))
  fs.append(cv('c · Boundary parametrization',[3*s.cos(t),3*s.sin(t),1-3*s.cos(t)-3*s.sin(t)] if k==11 else [s.cos(t),s.sin(t),s.sin(t)**2-s.cos(t)**2]))
 row(k,*fs,limited=k in(11,12,13,14,15),why='Stokes replaces the curl surface integral by circulation around the oriented boundary; a simpler spanning surface is valid only with the same oriented boundary.')
row(16,c('Area dependence','For positive normal(1,1,1)/√3, integral=(2/√3)Area; reverse orientation reverses the sign','Integral always equals0','Integral depends on perimeter'),limited=True)
row(19,c('Closed-sphere curl flux','Zero: split into two hemispheres; their boundary orientations oppose and cancel','4π times radius squared','Depends on the sphere radius'),limited=True)
row(20,c('a · Product curl','curl(f∇g)=∇f×∇g; apply Stokes','curl(f∇g)=f∇g','curl(f∇g)=∇g×∇f'),c('b · Integral','0 because∇f×∇f=0','Area(S)','Length(C)'),c('c · Integral','0 because f∇g+g∇f=∇(fg)','Area(S)','∫fgds'),limited=True)
A.row('unused',0) if False else None
qid='calculus-section-16-8-project-three-men-report';fields=[c('Relationship between the theorems','Green’s circulation theorem is the planar case of Stokes’ theorem, with upward normal','The two theorems contradict each other','Green’s theorem concerns only scalar limits'),c('Shared physical motivation','Electricity, magnetism and fluid circulation','Only counting permutations','Only discrete probability')]
for f0 in fields:f0.update(explanation='These checks assess the mathematical relationship and the source-stated motivation. A researched historical report and its citations require separate review.',provenance='explicit-source-inspected-original-answer-contract')
A.out[qid]=dict(grader=dict(type='parts',parts=fields,complete=False,scope='Checks two mathematical/contextual conclusions, not historical research quality or the written report.'),responsePartPrompt='Write the historical report requested in the complete source. These objective checks assess only the theorem relationship and motivation.',objectiveCheckVersion=4,objectiveChecksVerified=True,objectiveFieldCount=2,answerCheckSource=dict(type='source-reviewed-original-calculation',title='Stewart Calculus: Early Transcendentals, 8e',chapter=16,pages=[1171]));A.notes[qid]='Replaces eight bibliography records with the single actual unnumbered writing project; bibliography retained in source image.'
savepart('section08')
