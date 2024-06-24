import config from "./config";
import axios from "axios";
import Cookies from 'js-cookie'


export const register = async (userData) => {
    return axios.post(config.apiUrl + "/auth/signup", userData)
    .then(response => response.data)
    .catch(error => {
      console.error("Error signup:", error);
      throw error;
    });
}

export const login = async (userData) => {
    return axios.post(config.apiUrl + "/auth/login",
        userData,
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        })
      .then(response => {
        console.log(response.data)
        Cookies.set('token', response.data.access_token, { expires: 30 })
        return response.data
      })
      .catch(error => {
        console.error("Error login:", error);
      });
}


export const logout = () => {
    Cookies.set('token', '');
}

export const runTitleParser = async (resource) => {
    const token = 'Bearer ' + Cookies.get('token');
    return axios.post(
        config.apiUrl + '/posts/titles/test',
        {
            resources: [resource],
            urls: [],
            period_days: 10,
        },
        {
            headers: {
                'Authorization': token
            }
        }
    )
    .then(response => { return response.data })
    .catch(error => {
        console.error("Pars error!!!:", error);
    });
};


export const sendPostToTg = async (postId, url, post, title) => {
    const token = 'Bearer ' + Cookies.get('token');
    return axios.post(
        config.apiUrl + '/posts/telegram',
        {
            post_id: postId,
            url: url,
            post: post,
            title: title,
        },
        {
            headers: {
                'Authorization': token,
            }
        }
      ).then(response => {return response.data})
      .catch(error => {
        console.error("Pars error!!!:", error);
      });
}


export const deletePostById = async (postId) => {
    return axios.post(config.apiUrl + "/del", {"number": postId})
    .then(response => {
        return response.data
    })
    .catch(error => {
      console.error("Error fetching posts:", error);
    });
}


export const getAllTitles = () => {
    return axios.get(config.apiUrl + '/posts/titles')
    .then(response => {
        return response.data;
    })
    .catch(error => {
      console.error("Error fetching posts:", error);
    });
}

export const generatePost = async (url) => {
    const token = 'Bearer ' + Cookies.get('token');
    return axios.post(
        config.apiUrl + '/posts/article',
        {
            url: url,
        },
        {
            headers: {
                'Authorization': token,
            }
        }
      ).then(response => {
        return response.data;
      })
      .catch(error => {
        console.error("Pars error!!!:", error);
      });
}


export const addToFavorites = async (postId) => {
    return axios.post(config.apiUrl + "/favorites/create/", {number: postId})
        .then(response => {
            return response.data;
        })
        .catch(error => {
          console.error("Error adding to favorites: ", error);
        });
}

export const removeFromFavorites = async (postId) => {
    return axios.post(config.apiUrl + "/favorites/del/", {number: postId})
        .then(response => {
            return response.data;
        })
        .catch(error => {
          console.error("Error deleting from favorites: ", error);
        });
}