<template>
  <div class="d-flex flex-column align-items-center">
    <div class="position-absolute langs-enabler" @mousedown="toggleLangsDisplay" @touchstart="toggleLangsDisplay"></div>
    <div class="position-absolute langs text-l" :style="{opacity: langsOpacity}">
      <span class="mr-4" @mousedown="setLang('fr')" @touchstart="setLang('fr')">FR</span>
      <span @mousedown="setLang('en')" @touchstart="setLang('en')">EN</span>
    </div>
    <div class="d-flex flex-column align-items-center my-xl">
      <div class="text-xxl text-teal drop-shadow-teal text-name-smile">
        {{ $t('the_digimiam') }}
      </div>
      <div class="text-xl text-orange drop-shadow-orange text-las-enter">
        {{ $t('subtitle') }}
      </div>
    </div>
  </div>
</template>

<script>
import publishSubscribeService from '@/store/publishSubscribeService.js'

export default {
  name: "Title",
  data() {
    return {
      langsOpacity: 0,
    }
  },
  methods: {
    toggleLangsDisplay() {
      this.langsOpacity = this.langsOpacity === 1 ? 0 : 1
    },
    setLang(lang) {
      publishSubscribeService.commit('publish', {category: "localize", value: lang})
    },
  },
}
</script>

<style scoped>
.my-xl {
  margin-bottom: 90px;
  margin-top: 90px;
}

.langs {
  top: 10px;
  right: 20px;
  font-size: 30px;
  transition: opacity 1s ease-in-out;
}

.langs-enabler {
  top: 0px;
  left: 0px;
  width: 50px;
  height: 50px;
}
</style>