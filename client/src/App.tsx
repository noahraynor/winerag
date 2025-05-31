import { useState } from 'react';

const App = () => {
  return (
    <>
      <h1>WineRag App</h1>
      <WineInput />
    </>
  );
};

const WineInput = () => {
  const [userInput, setUserInput] = useState('');

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>): void => {
    setUserInput(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>): void => {
    e.preventDefault();
  }

  return (
    <>
    <form onSubmit={(e) => handleSubmit(e)}>
      <label htmlFor="wineTourInput">Describe your dream wine tour:</label>
      <input
        id="wineTourInput"
        type="text"
        value={userInput}
        onChange={(e) => handleInputChange(e)}
      />
      <button type="submit">Submit</button>
    </form>

    </>
  );
}

export default App;
