export const API=process.env.NEXT_PUBLIC_API_URL||"http://127.0.0.1:8000";
export async function api(path:string,opt:RequestInit={}){
  const headers:Record<string,string>={};
  if(!(opt.body instanceof FormData)) headers["Content-Type"]="application/json";
  const r=await fetch(API+path,{...opt,headers:{...headers,...(opt.headers||{})},cache:"no-store"});
  if(!r.ok) throw new Error(await r.text());
  return r.json();
}