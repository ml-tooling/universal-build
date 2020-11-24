import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

jest.mock('react-i18next', () => ({
  // this mock makes sure any components using the translate hook can use it without that a warning is thrown as no i18n object is provided during the tests
  useTranslation: () => {
    return {
      t: (str) => str,
      i18n: {
        changeLanguage: () => new Promise(() => {}),
      },
    };
  },
}));

test('renders learn react link', () => {
  render(<App />);
  const linkElement = screen.getByText(/learn react/i);
  expect(linkElement).toBeInTheDocument();
});
