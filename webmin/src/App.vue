<template>
  <div id="app" class="d-flex flex-row flex-grow-1">
    <Nav class="flex-shrink-0"></Nav>

    <router-view class="bgc-softdark flex-grow-1"></router-view>
  </div>
</template>

<script>
import Vue from 'vue'
import axios from 'axios'
import Nav from '@/components/nav/Nav.vue'
import roomStore from '@/store/roomStore.js'
import 'vue-select/dist/vue-select.css'

export default {
  name: 'App',
  components: {Nav},
  created() {
    let storage_url = this.$route.query.storage_url
    if (storage_url) {
      Vue.prototype.$justRestAPI = axios.create({
        baseURL: 'http://' + storage_url
      })
    } else {
      Vue.prototype.$justRestAPI = axios.create({
        baseURL: 'http://justrelax.justescape:8000'
      })
    }

    roomStore.dispatch('fetchRooms')
    // roomStore.dispatch('fetchRuleSets')

    let ws_url = this.$route.query.ws_url
    if (ws_url) {
      this.$connect('ws://' + ws_url)
    } else {
      this.$connect('ws://justrelax.justescape:3032')
    }
  }
}
</script>

<style>
@font-face {
    font-family: "Big Noodle";
    font-style: normal;
    font-display: swap;
    src: url('./assets/font/big-noodle.eot');
    src:
      url('./assets/font/big-noodle.eot?#iefix') format('embedded-opentype'),
      url('./assets/font/big-noodle.woff2') format('woff2'),
      url('./assets/font/big-noodle.woff') format('woff'),
      url('./assets/font/big-noodle.ttf') format('truetype');
    unicode-range: U+000-5FF, U+20AC; /* Latin */
}

@font-face {
    font-family: "Big Noodle";
    font-style: oblique;
    font-display: swap;
    src: url('./assets/font/big-noodle-oblique.eot');
    src:
      url('./assets/font/big-noodle-oblique.eot?#iefix') format('embedded-opentype'),
      url('./assets/font/big-noodle-oblique.woff2') format('woff2'),
      url('./assets/font/big-noodle-oblique.woff') format('woff'),
      url('./assets/font/big-noodle-oblique.ttf') format('truetype');
    unicode-range: U+000-5FF; /* Latin */
}

@font-face {
    font-family: "Roboto";
    font-style: normal;
    font-weight: 400;
    font-display: swap;
    src: url('./assets/font/roboto-v19-latin-regular.eot');
    src:
      local('Roboto'),
      local('Roboto-Regular'),
      url('./assets/font/roboto-v19-latin-regular.woff2') format('woff2'),
      url('./assets/font/roboto-v19-latin-regular.woff') format('woff'),
      url('./assets/font/roboto-v19-latin-regular.ttf') format('truetype');
    unicode-range: U+000-5FF, U+20AC; /* Latin */
}

body {
  min-height: 100%;
}

#app {
  font-family: "Lato", "Helvetica", "Arial", "sans-serif";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.big-noodle {
  font-family: "Big Noodle", "Helvetica", "Arial", "sans-serif";
}

.oblique {
  font-style: oblique;
}

.text-jaffa {
  color: #f38d40;
}

.text-mulberry {
  color: #cb4299;
}

.text-grey {
  color: #949497;
}

.text-underline {
  text-decoration: underline;
}

.h-75px {
  height: 75px;
}

a {
  color: inherit;
}

a:hover {
  color: inherit;
  text-decoration: none;
}

.bgc-dark {
  background-color: #3c3c3e;
  color: #f8f9fa;
}

.bgc-deepdark {
  background-color: #2e2e2e;
  color: #f8f9fa;
}

.bgc-softdark {
  background-color: #4d4d4f;
  color: #f8f9fa;
}

.pointer:hover {
  cursor: pointer;
}

.border-jaffa {
  border: 1px #f38d40 solid;
}

.size-25 {
  font-size: 2.5rem;
}

.size-15 {
  font-size: 1.5rem;
}

.lh-15 {
  line-height: 1.5;
}

.top-0 {
  top: 0;
}

input.form-control, select.form-control, textarea.form-control, .input-group > .input-group-append > .input-group-text {
    background: transparent;
    border-color: #f38d40;
    color: #f8f9fa;
}

select.form-control {
  background: transparent;
  background-image: url("data:image/svg+xml;utf8,<svg fill='black' height='24' viewBox='0 0 24 24' width='24' xmlns='http://www.w3.org/2000/svg'><path fill='rgb(243, 141, 64)' d='M7 10l5 5 5-5z'/><path d='M0 0h24v24H0z' fill='none'/></svg>");
  background-repeat: no-repeat;
  background-position-x: 100%;
  background-position-y: 5px;
}

.custom-file-label {
  background: transparent;
  border-color: #f38d40;
  color: #949497;
}

.custom-file-label::after {
  color: #f38d40;
  background-color: transparent;
}

.custom-file-input:hover {
  cursor: pointer;
}

.custom-file-label:focus, .custom-file-input:focus {
  outline-color: transparent;
}

.custom-file-input:focus ~ .custom-file-label {
  box-shadow: none;
  border-color: #f38d40;
}

input.form-control:focus, select.form-control:focus, textarea.form-control:focus {
    box-shadow: 0 0 0 0.2rem rgba(243, 141, 64, 0.25);
    background-color: transparent;
    border-color: #f38d40;
    color: #f8f9fa;
}

input.form-control::placeholder {
    color: #949497;
}

.border-deepdark {
  border: 1px #2e2e2e solid;
}

table {
  width: auto;
}

thead {
  background-color: #2e2e2e;
  color: #f38d40;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #3c3c3e;
  color: #f8f9fa;
}

.table-striped tbody tr:nth-of-type(even) {
  background-color: transparent;
  color: #f8f9fa;
}

.padding-bottom-10rem {
  padding-bottom: 10rem;
}

.text-one-line-ellipsis {
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  display: -webkit-box;
}

@media (pointer: coarse), (hover: none) {
  [title]:active::after {
    content: attr(title);
    position: absolute;
    top: 90%;
    color: var(--light);
    background-color: var(--dark);
    border: 1px solid;
    width: fit-content;
    padding: 3px;
  }
}

.min-width-100px {
  min-width: 100px;
}
</style>
