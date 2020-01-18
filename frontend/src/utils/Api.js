import axios from 'axios';

import config from '../config';

const downloadData = async (endpoint, params) => {
  let url;
  if (config.ENVDEV) {
    url = `${config.APIURL}/${endpoint}`;
  } else {
    url = `${config.APIREMOTEURL}/${endpoint}`;
  }
  try {
    const response = await axios.get(url, { params });
    return response.data;
  } catch (err) {
    return;
  }
};

export default downloadData;
