import axios from 'axios';

import config from '../config';

const downloadData = async (endpoint, params) => {
  let url;
  if (config.ENVDEV) {
    url = `${config.APIURL}/${endpoint}`;
  } else {
    url = `${config.APIREMOTEURL}/${endpoint}`;
  }
  console.log('url', url);
  console.log('params', params);
  const response = await axios.get(url, { params });
  console.log('response.data', response.data);
  return response.data;
};

export default downloadData;
