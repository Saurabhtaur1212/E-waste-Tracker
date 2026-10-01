"use client";
import Link from "next/link";
import {Leaf,LayoutDashboard,ScanLine,Recycle,Trash2,Users,LogIn} from "lucide-react";
export default function Nav(){
 const items=[[ScanLine,"Scan","/"],[Recycle,"E-Waste","/ewaste"],[Trash2,"Bins","/bins"],[Users,"Community","/community"],[LayoutDashboard,"Command","/dashboard"]];
 return <header className="sticky top-0 z-50 border-b border-[#dce6df] bg-white/95 backdrop-blur-xl"><div className="mx-auto flex max-w-7xl items-center justify-between px-5 py-4"><Link href="/" className="text-xl font-black"><span className="mr-2 inline-block rounded-xl bg-green-400/10 p-2 text-green-400"><Leaf size={19}/></span>Green<span className="text-green-400">Trace</span><span className="ml-2 text-xs text-slate-500">PRO</span></Link><nav className="hidden gap-1 md:flex">{items.map(([I,t,h]:any)=><Link className="btn hover:bg-emerald-50" href={h} key={t}><I size={15} className="mr-1 inline"/>{t}</Link>)}<Link className="btn border border-[#dce6df]" href="/login"><LogIn size={15} className="mr-1 inline"/>Login</Link></nav></div></header>
}