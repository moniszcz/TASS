import React from 'react';
import { ToastContainer, toast } from 'react-toastify';

const createNoDataToast = () =>
  toast.info('No data for current query 😟!', {
    position: 'top-right',
    autoClose: 2000,
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true
  });

const createLoadingDataToast = () => {
  toast.info('Loading data 🤔', {
    position: 'top-right',
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true
  });
};

const dismissToasts = () => {
  toast.dismiss();
};

const getToastContainer = () => (
  <ToastContainer
    position="top-right"
    autoClose={false}
    hideProgressBar={false}
    newestOnTop={false}
    closeOnClick
    rtl={false}
    pauseOnVisibilityChange={false}
    draggable
    pauseOnHover
  />
);

export {
  createNoDataToast,
  getToastContainer,
  createLoadingDataToast,
  dismissToasts
};
