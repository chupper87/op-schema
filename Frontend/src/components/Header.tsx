import waveImg from "../assets/wave.png";
import { HouseLine, Gear, User, FirstAid, Users, ClipboardText, ChartBar, Calendar } from "phosphor-react";

export function Header() {
  return (
    <div className="flex flex-col">
        <div className="flex flex-row items-center w-full h-18 bg-indigo-900 px-10">
            <h1 className="text-3xl font-bold text-white">Timepiece</h1>
            <img className="h-8 w-8 ml-2" src={waveImg} alt="wave" />
            
            
            <div className="flex ml-120 space-x-8">
                <div className="flex flex-col items-center cursor-pointer group bg-transparent hover:bg-indigo-800 p-2 rounded-md transition-colors">
                    <FirstAid size={30} color="#FF6B8B" weight="fill" />
                    <span className="text-white text-sm mt-1">Vårdtagare</span>
                </div>
                
                <div className="flex flex-col items-center cursor-pointer group bg-transparent hover:bg-indigo-800 p-2 rounded-md transition-colors">
                    <Users size={30} color="#64B5F6" weight="fill" />
                    <span className="text-white text-sm mt-1">Medarbetare</span>
                </div>

                <div className="flex flex-col items-center cursor-pointer group bg-transparent hover:bg-indigo-800 p-2 rounded-md transition-colors">
                    <Calendar size={30} color="#FFFFFF" weight="fill" />
                    <span className="text-white text-sm mt-1">Planering</span>
                </div>
                
                <div className="flex flex-col items-center cursor-pointer group bg-transparent hover:bg-indigo-800 p-2 rounded-md transition-colors">
                    <ClipboardText size={30} color="#FFD54F" weight="fill" />
                    <span className="text-white text-sm mt-1">Insatser</span>
                </div>
                
                <div className="flex flex-col items-center cursor-pointer group bg-transparent hover:bg-indigo-800 p-2 rounded-md transition-colors">
                    <ChartBar size={30} color="#81C784" weight="fill" />
                    <span className="text-white text-sm mt-1">Statistik</span>
                </div>
                
                
            </div>
            
            
            
            <div className="flex justify-right absolute right-10 space-x-8">
                <HouseLine size={28} color="#87bafa" weight="fill" className="hover:opacity-80 cursor-pointer" />
                <Gear size={28} color="#d7dbd8" weight="fill" className="hover:opacity-80 cursor-pointer" />
                <User size={28} color="#b4fac5" weight="fill" className="hover:opacity-80 cursor-pointer" />
            </div>
        </div>      
    </div>
  )
}

export default Header;