import { NavLink } from "react-router-dom";
import waveImg from "../assets/wave.png";
import { HouseLine, Gear, User, FirstAid, Users, ClipboardText, ChartBar, Calendar } from "phosphor-react";

export function Header() {
  return (
    <div className="flex flex-col">
        <div className="flex flex-row items-center justify-between w-full h-18 bg-indigo-900 px-4 md:px-10">
            {/* Vänster: Logo */}
            <div className="flex items-center">
                <h1 className="text-xl md:text-2xl lg:text-3xl font-bold text-white">Timepiece</h1>
                <img className="h-6 w-6 md:h-8 md:w-8 ml-2" src={waveImg} alt="wave" />
            </div>

            {/* Mitten: Navigering - dölj på små skärmar */}
            <div className="hidden lg:flex space-x-4 xl:space-x-8">
                <NavLink
                    to="/customers"
                    className={({ isActive }) =>
                        `flex flex-col items-center cursor-pointer group p-2 rounded-md transition-colors ${
                            isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
                        }`
                    }
                >
                    <FirstAid size={24} className="lg:w-[30px] lg:h-[30px]" color="#FF6B8B" weight="fill" />
                    <span className="text-white text-xs lg:text-sm mt-1">Vårdtagare</span>
                </NavLink>

                <NavLink
                    to="/employees"
                    className={({ isActive }) =>
                        `flex flex-col items-center cursor-pointer group p-2 rounded-md transition-colors ${
                            isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
                        }`
                    }
                >
                    <Users size={24} className="lg:w-[30px] lg:h-[30px]" color="#64B5F6" weight="fill" />
                    <span className="text-white text-xs lg:text-sm mt-1">Medarbetare</span>
                </NavLink>

                <NavLink
                    to="/schedule"
                    className={({ isActive }) =>
                        `flex flex-col items-center cursor-pointer group p-2 rounded-md transition-colors ${
                            isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
                        }`
                    }
                >
                    <Calendar size={24} className="lg:w-[30px] lg:h-[30px]" color="#FFFFFF" weight="fill" />
                    <span className="text-white text-xs lg:text-sm mt-1">Planering</span>
                </NavLink>

                <NavLink
                    to="/measures"
                    className={({ isActive }) =>
                        `flex flex-col items-center cursor-pointer group p-2 rounded-md transition-colors ${
                            isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
                        }`
                    }
                >
                    <ClipboardText size={24} className="lg:w-[30px] lg:h-[30px]" color="#FFD54F" weight="fill" />
                    <span className="text-white text-xs lg:text-sm mt-1">Insatser</span>
                </NavLink>

                <NavLink
                    to="/statistics"
                    className={({ isActive }) =>
                        `flex flex-col items-center cursor-pointer group p-2 rounded-md transition-colors ${
                            isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
                        }`
                    }
                >
                    <ChartBar size={24} className="lg:w-[30px] lg:h-[30px]" color="#81C784" weight="fill" />
                    <span className="text-white text-xs lg:text-sm mt-1">Statistik</span>
                </NavLink>


            </div>

            {/* Höger: Ikoner */}
            <div className="flex space-x-4 md:space-x-8">
                <NavLink to="/home">
                    <HouseLine size={20} className="md:w-[28px] md:h-[28px]" color="#87bafa" weight="fill" />
                </NavLink>
                <Gear size={20} className="md:w-[28px] md:h-[28px] hover:opacity-80 cursor-pointer" color="#d7dbd8" weight="fill" />
                <User size={20} className="md:w-[28px] md:h-[28px] hover:opacity-80 cursor-pointer" color="#b4fac5" weight="fill" />
            </div>
        </div>
    </div>
  )
}

export default Header;
