"use client";
import {useState} from "react";
import {useRouter} from "next/navigation";
import {GraduationCap,ShieldCheck} from "lucide-react";
import {api} from "../../lib/api";

type AccessType="admin"|"student";

const demoAccounts={
  admin:{email:"admin@example.com",password:"admin123"},
  student:{email:"student@example.com",password:"student123"}
};

export default function Login(){
  const[access,setAccess]=useState<AccessType>("student");
  const[email,setEmail]=useState(demoAccounts.student.email);
  const[password,setPassword]=useState(demoAccounts.student.password);
  const[err,setErr]=useState("");
  const router=useRouter();

  function chooseAccess(type:AccessType){
    setAccess(type);
    setEmail(demoAccounts[type].email);
    setPassword(demoAccounts[type].password);
    setErr("");
  }

  async function submit(event:React.FormEvent<HTMLFormElement>){
    event.preventDefault();
    setErr("");
    try{
      const user=await api("/api/auth/login",{
        method:"POST",
        body:JSON.stringify({email,password})
      });
      if(user.role!==access){
        setErr(`This account does not have ${access==="admin"?"Admin":"Student / Customer"} access.`);
        return;
      }
      localStorage.setItem("greentrace_user",JSON.stringify(user));
      router.push(access==="admin"?"/dashboard":"/community");
    }catch{
      setErr("Unable to sign in. Check your email and password.");
    }
  }

  return <section className="mx-auto max-w-md px-5 py-16 sm:py-20">
    <div className="card p-6 sm:p-8">
      <p className="text-xs font-bold tracking-[.14em] text-green-400">GREENTRACE ACCESS</p>
      <h1 className="mt-2 text-3xl font-black">Sign in</h1>
      <p className="mt-2 text-sm text-slate-500">Choose the access that matches your account.</p>

      <div className="mt-6 grid grid-cols-2 gap-2 rounded-xl bg-[#edf3ef] p-1" aria-label="Choose account type">
        <button type="button" onClick={()=>chooseAccess("admin")} aria-pressed={access==="admin"} className={`flex min-h-12 items-center justify-center gap-2 rounded-lg px-3 text-sm font-bold transition ${access==="admin"?"bg-white text-green-800 shadow-sm":"text-slate-500 hover:text-slate-800"}`}>
          <ShieldCheck size={17}/> Admin
        </button>
        <button type="button" onClick={()=>chooseAccess("student")} aria-pressed={access==="student"} className={`flex min-h-12 items-center justify-center gap-2 rounded-lg px-2 text-sm font-bold transition ${access==="student"?"bg-white text-green-800 shadow-sm":"text-slate-500 hover:text-slate-800"}`}>
          <GraduationCap size={17}/> Student / Customer
        </button>
      </div>

      <form onSubmit={submit} className="mt-6 space-y-4">
        <label className="block text-sm font-semibold" htmlFor="email">Email address</label>
        <input id="email" type="email" autoComplete="username" required className="-mt-2 w-full rounded-xl border border-[#dce6df] bg-white p-3 text-[#17231d] placeholder:text-slate-400 focus:border-green-600 focus:ring-2 focus:ring-green-100" value={email} onChange={event=>setEmail(event.target.value)}/>
        <label className="block text-sm font-semibold" htmlFor="password">Password</label>
        <input id="password" type="password" autoComplete="current-password" required className="-mt-2 w-full rounded-xl border border-[#dce6df] bg-white p-3 text-[#17231d] placeholder:text-slate-400 focus:border-green-600 focus:ring-2 focus:ring-green-100" value={password} onChange={event=>setPassword(event.target.value)}/>
        <button className="btn w-full bg-green-400 text-black">Sign in as {access==="admin"?"Admin":"Student / Customer"}</button>
      </form>
      {err&&<p role="alert" className="mt-4 text-sm text-red-300">{err}</p>}
      <p className="mt-5 border-t border-[#dce6df] pt-4 text-xs text-slate-500">
        Demo: {demoAccounts[access].email} / {demoAccounts[access].password}
      </p>
    </div>
  </section>;
}