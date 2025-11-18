import { useState } from 'react';
import { Link } from 'react-router-dom';
import waveImg from '../../../assets/wave.png';
import Button from '../../../components/Button';
import { useAuth } from '../hooks/useAuth';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    console.log('Login with:', email, password);
    login({ username: email, password: password });
  };
  const { login, isLoading, error } = useAuth();

  return (
    <div className="flex flex-col items-center justify-center">
      <div className="flex flex-row items-center justify-center">
        <h1 className="dark:text-indigo m-3.5 text-5xl font-extrabold text-indigo-900">
          Timepiece
        </h1>
        <img className="mb-5 h-15 w-15 items-center justify-center pt-2" src={waveImg} alt="wave" />
      </div>

      <form onSubmit={handleSubmit}>
        <label
          htmlFor="username"
          className="dark:text-indigo mb-2 block pt-5 text-sm font-bold text-indigo-900"
        >
          Username
        </label>
        <input
          type="username"
          id="username"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="block rounded-lg border-1 border-indigo-900 bg-white p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-indigo-900 dark:bg-white dark:text-indigo-900 dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
          placeholder="username"
          required
        />
        <label
          htmlFor="password"
          className="dark:text-indigo block pt-1 text-sm font-bold text-indigo-900"
        >
          Password
        </label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          className="block rounded-lg border-1 border-indigo-900 bg-white p-2.5 text-sm text-gray-900 focus:border-blue-500 focus:ring-blue-500 dark:border-indigo-900 dark:bg-white dark:text-indigo-900 dark:placeholder-gray-400 dark:focus:border-blue-500 dark:focus:ring-blue-500"
          required
        />
        <a
          href="#"
          className="dark:text-indigo mt-2 block text-xs text-indigo-900 hover:text-indigo-600"
        >
          Forgot password?
        </a>
        <div className="mt-4 flex justify-center">
          <Button disabled={isLoading} />
        </div>
        <div className="mt-2 flex justify-center">
          {error && <p className="items-center justify-center text-red-500">Login failed</p>}
        </div>

        <div className="mt-2 flex justify-center">
          <Link
            to="/register"
            className="dark:text-indigo text-xs text-indigo-900 hover:text-indigo-600"
          >
            Create account
          </Link>
        </div>
      </form>
    </div>
  );
}
