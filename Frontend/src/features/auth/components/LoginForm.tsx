import { useState } from "react";
import { Link } from "react-router-dom";
import waveImg from "../../../assets/wave.png";
import Button from "../../../components/Button";

export default function LoginForm() {

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("Login with:", email, password);
    };

    return (
        <div className="flex flex-col items-center justify-center">
            <div className="flex flex-row items-center justify-center">
                <h1 className="m-3.5 text-indigo-900 font-bold text-5xl">Timepiece</h1>
                <img  className="h-15 w-15 justify-center items-center mb-5 pt-2" src={waveImg} alt="wave" />
            </div>
            
            <form onSubmit={handleSubmit}>
                <label htmlFor="email" className="block mb-2 text-sm font-bold text-indigo-900 dark:text-indigo pt-5">Username</label>
                <input 
                    type="email" 
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    className="bg-white border-1 border-indigo-900 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-white dark:border-indigo-900 dark:placeholder-gray-400 dark:text-indigo-900 dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                    placeholder="email@example.com" 
                    required 
                />
                <label htmlFor="password" className="block text-sm font-bold text-indigo-900 dark:text-indigo pt-1">Password</label>
                <input 
                    type="password" 
                    id="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    className="bg-white border-1 border-indigo-900 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block p-2.5 dark:bg-white dark:border-indigo-900 dark:placeholder-gray-400 dark:text-indigo-900 dark:focus:ring-blue-500 dark:focus:border-blue-500" 
                    required 
                />
                <a href="#" className="text-xs text-indigo-900 dark:text-indigo mt-2 block hover:text-indigo-600">Forgot password?</a>
                <div className="flex justify-center mt-4">
                    <Button />
                </div>

                <div className="flex justify-center mt-2">
                    <Link to="/register" className="text-indigo-900 dark:text-indigo text-xs hover:text-indigo-600">Create account</Link>
                </div>
            </form>
        </div>
    );
}



