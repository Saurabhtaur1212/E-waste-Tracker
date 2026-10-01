import "./globals.css";
import Nav from "../components/Nav";
export const metadata={title:"GreenTrace Pro",description:"Smart Waste and E-Waste Intelligence"};
export default function Root({children}:{children:React.ReactNode}){return <html><body><Nav/>{children}</body></html>}