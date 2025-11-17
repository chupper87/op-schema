


export default function WelcomeMessage({ userName }: { userName: string }) {
    return (
        <div>
            <h1 className="text-3xl font-bold text-indigo-900 pt-10">Välkommen {userName}!</h1>
        </div>
    );
}
