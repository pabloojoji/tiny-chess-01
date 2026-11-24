import os,json,urllib.request as u
V=[0,100,320,330,500,900,0];N=[-33,-31,-18,-14,14,18,31,33];K=[-17,-16,-15,-1,1,15,16,17];D=[-17,-15,15,17];O=[-16,-1,1,16];S0="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
T=[[0]*64 for _ in range(7)]
for p in range(1,7):
 for s in range(64):
  f=s%8;r=s//8;c=int(3.5-abs(f-3.5)-abs(r-3.5));T[p][s]=[r*9,c*9,c*6,14 if r==6 else 0,c*3,-c*10][p-1]
DI={2:N,3:D,4:O,5:D+O,6:K}
def F(f):
 b=[0]*120;p=f.split();r=7;c=0
 for ch in p[0]:
  if ch=='/':r-=1;c=0
  elif ch.isdigit():c+=int(ch)
  else:b[r*16+c]=('PNBRQK'.find(ch.upper())+1)*(1 if ch.isupper() else -1);c+=1
 return b,p[1]=='w',(int(p[3][1])-1)*16+ord(p[3][0])-97 if len(p)>3 and p[3]!='-' else -1
def A(b,s,w):
 p=1 if w else -1
 for o in(15,17):
  t=s-o*p
  if 0<=t<120 and not t&136 and b[t]==p:return 1
 for o in N:
  t=s+o
  if 0<=t<120 and not t&136 and b[t]==p*2:return 1
 for o in K:
  t=s+o
  if 0<=t<120 and not t&136 and b[t]==p*6:return 1
 for o in D+O:
  t=s+o
  while 0<=t<120 and not t&136:
   if b[t]:return 1 if b[t]==p*5 or(o in D and b[t]==p*3)or(o in O and b[t]==p*4)else 0
   t+=o
 return 0
def M(b,m,w,e):
 s=m//128;t=m%128;n=b[:];v=n[s];n[s]=0
 if abs(v)==1 and t==e:n[t-(16 if w else -16)]=0
 n[t]=(5 if w else -5) if abs(v)==1 and(t>>4)==(7 if w else 0)else v
 if abs(v)==6 and abs(t-s)==2:
  if t>s:n[t-1]=n[t+1];n[t+1]=0
  else:n[t+1]=n[t-2];n[t-2]=0
 return n,(s+t)//2 if abs(v)==1 and abs(t-s)==32 else -1
def G(b,w,e):
 m=[];p=1 if w else -1;d=16*p
 for s,v in enumerate(b):
  if s&136 or v*p<=0:continue
  a=abs(v);r=s>>4
  if a==1:
   t=s+d
   if not t&136 and not b[t]:
    m.append(s*128+t)
    if(r==1 if w else r==6)and not b[s+2*d]:m.append(s*128+s+2*d)
   for o in(d-1,d+1):
    t=s+o
    if not t&136 and(b[t]*p<0 or t==e)and abs(b[t])!=6:m.append(s*128+t)
  else:
   for o in DI[a]:
    t=s+o
    while not t&136:
     if b[t]*p>0 or abs(b[t])==6:break
     m.append(s*128+t)
     if b[t] or a in(2,6):break
     t+=o
 o=[]
 for mv in m:
  nb,_=M(b,mv,w,e);ks=next(i for i,v in enumerate(nb) if v==(6 if w else -6))
  if not A(nb,ks,not w):o.append(mv)
 return o
def E(b,w):
 s=0
 for i,v in enumerate(b):
  if v and not i&136:
   a=abs(v);rr=(i>>4) if v>0 else 7-(i>>4);s+=(V[a]+T[a][(i&7)+rr*8])*(1 if v>0 else -1)
 return s if w else -s
ND=[0]
def S(b,w,e,d,a,be,pl):
 ND[0]+=1
 if ND[0]>20000:return E(b,w)
 if d<=0:
  s=E(b,w)
  if s>=be:return s
  a=max(a,s)
  for m in [m for m in G(b,w,e) if b[m%128]]:
   nb,ne=M(b,m,w,e);sc=-S(nb,not w,ne,0,-be,-a,pl+1)
   if sc>a:a=sc
   if a>=be:return a
  return a
 ms=G(b,w,e)
 if not ms:
  ks=next(i for i,v in enumerate(b) if v==(6 if w else -6));return -100000+pl if A(b,ks,not w) else 0
 ms.sort(key=lambda m:-(V[abs(b[m%128])]*10 if b[m%128] else 0));best=-1000000
 for m in ms:
  nb,ne=M(b,m,w,e);sc=-S(nb,not w,ne,d-1,-be,-a,pl+1)
  if sc>best:best=sc
  if best>=be:break
  a=max(a,best)
 return best
def R(b,w,e):
 ms=G(b,w,e);best=ms[0];bs=-1000000
 for m in ms:
  nb,ne=M(b,m,w,e);sc=-S(nb,not w,ne,3,-1000000,-bs,1)
  if sc>bs:bs=sc;best=m
 return best,bs
U=lambda m:chr(97+(m//128&7))+str((m//128>>4)+1)+chr(97+(m%128&7))+str((m%128>>4)+1)
Z=lambda m,b:U(m)+('q' if b[m//128] in(1,-1) and(m%128>>4)in(0,7)else '')
def Y(b,w,e,u):
 s=(ord(u[0])-97)+(int(u[1])-1)*16;t=(ord(u[2])-97)+(int(u[3])-1)*16;return M(b,s*128+t,w,e),not w
def P(p,d):
 try:
  r=u.Request(os.environ['MAKEFUN_ENV_URL'].rstrip('/')+p,data=json.dumps(d).encode(),headers={'Content-Type':'application/json'},method='POST')
  with u.urlopen(r,timeout=5) as x:return json.loads(x.read() or b'{}')
 except Exception:return {}
def main():
 if 'MAKEFUN_ENV_URL' not in os.environ:
  b,w,e=F(os.environ.get('TEST_FEN',S0));m,s=R(b,w,e);print(Z(m,b) if m else '0000',s);return
 g=P('/game',{});gid=g.get('game') or g.get('id') or '';b,w,e=F(g.get('fen') or S0)
 if g.get('move'):(b,e),w=Y(b,w,e,g['move'])
 while True:
  m,s=R(b,w,e)
  if not m:break
  r=P('/move',{'game':gid,'move':Z(m,b)})
  om=r.get('move') or r.get('opponent_move') or r.get('reply')
  if not om:break
  (b,e),w=M(b,m,w,e),not w;(b,e),w=Y(b,w,e,om)
main()
