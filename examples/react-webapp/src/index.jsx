import React, { Suspense } from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './pages/App';
import reportWebVitals from './utils/reportWebVitals';

// import i18n (needs to be bundled ;))
import './i18n';

ReactDOM.render(
  <React.StrictMode>
    {/* Suspense is used because otherwise i18n will throw an error. See  */}
    <Suspense fallback="">
      <App />
    </Suspense>
  </React.StrictMode>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
