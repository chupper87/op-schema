import { NavLink } from 'react-router-dom';
import waveImg from '../assets/wave.png';
import {
  HouseLine,
  Gear,
  User,
  FirstAid,
  Users,
  ClipboardText,
  ChartBar,
  Calendar,
} from 'phosphor-react';

export function Header() {
  return (
    <div className="flex flex-col">
      <div className="flex h-18 w-full flex-row items-center justify-between bg-indigo-900 px-4 md:px-10">
        {/* Vänster: Logo */}
        <div className="flex items-center">
          <NavLink to="/home">
            <h1 className="text-xl font-bold text-white md:text-2xl lg:text-3xl">Timepiece</h1>
          </NavLink>
          <img className="ml-2 h-6 w-6 md:h-8 md:w-8" src={waveImg} alt="wave" />
        </div>

        {/* Mitten: Navigering - dölj på små skärmar */}
        <div className="hidden space-x-4 lg:flex xl:space-x-8">
          <NavLink
            to="/customers"
            className={({ isActive }) =>
              `group flex cursor-pointer flex-col items-center rounded-md p-2 transition-colors ${
                isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
              }`
            }
          >
            <FirstAid size={24} className="lg:h-[30px] lg:w-[30px]" color="#FF6B8B" weight="fill" />
            <span className="mt-1 text-xs text-white lg:text-sm">Vårdtagare</span>
          </NavLink>

          <NavLink
            to="/employees"
            className={({ isActive }) =>
              `group flex cursor-pointer flex-col items-center rounded-md p-2 transition-colors ${
                isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
              }`
            }
          >
            <Users size={24} className="lg:h-[30px] lg:w-[30px]" color="#64B5F6" weight="fill" />
            <span className="mt-1 text-xs text-white lg:text-sm">Medarbetare</span>
          </NavLink>

          <NavLink
            to="/schedule"
            className={({ isActive }) =>
              `group flex cursor-pointer flex-col items-center rounded-md p-2 transition-colors ${
                isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
              }`
            }
          >
            <Calendar size={24} className="lg:h-[30px] lg:w-[30px]" color="#FFFFFF" weight="fill" />
            <span className="mt-1 text-xs text-white lg:text-sm">Planering</span>
          </NavLink>

          <NavLink
            to="/measures"
            className={({ isActive }) =>
              `group flex cursor-pointer flex-col items-center rounded-md p-2 transition-colors ${
                isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
              }`
            }
          >
            <ClipboardText
              size={24}
              className="lg:h-[30px] lg:w-[30px]"
              color="#FFD54F"
              weight="fill"
            />
            <span className="mt-1 text-xs text-white lg:text-sm">Insatser</span>
          </NavLink>

          <NavLink
            to="/statistics"
            className={({ isActive }) =>
              `group flex cursor-pointer flex-col items-center rounded-md p-2 transition-colors ${
                isActive ? 'bg-indigo-700' : 'bg-transparent hover:bg-indigo-800'
              }`
            }
          >
            <ChartBar size={24} className="lg:h-[30px] lg:w-[30px]" color="#81C784" weight="fill" />
            <span className="mt-1 text-xs text-white lg:text-sm">Statistik</span>
          </NavLink>
        </div>

        {/* Höger: Ikoner */}
        <div className="flex space-x-4 md:space-x-8">
          <NavLink to="/home">
            <HouseLine
              size={20}
              className="md:h-[28px] md:w-[28px]"
              color="#87bafa"
              weight="fill"
            />
          </NavLink>
          <Gear
            size={20}
            className="cursor-pointer hover:opacity-80 md:h-[28px] md:w-[28px]"
            color="#d7dbd8"
            weight="fill"
          />
          <User
            size={20}
            className="cursor-pointer hover:opacity-80 md:h-[28px] md:w-[28px]"
            color="#b4fac5"
            weight="fill"
          />
        </div>
      </div>
    </div>
  );
}

export default Header;
