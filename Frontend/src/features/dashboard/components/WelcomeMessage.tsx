export default function WelcomeMessage({ userName }: { userName: string }) {
  return (
    <div>
      <h1 className="pt-10 text-3xl font-bold text-indigo-900">Välkommen {userName}!</h1>
    </div>
  );
}
