<template>
  <div class="frame mt-5 position-relative">
    <div class="d-flex flex-row justify-content-between position-absolute w-100 pointer-events-none">
      <div>
        <FramedButton
          :style="{'transform': 'translateX(' + easyTranslateX + 'px)'}"
          class="text-l mr-2 transition-transform pointer-events-auto"
          :fill="difficulty === 'easy'" :label="$t('easy')"
          @mousedown="setDifficulty('easy')"
        />
        <FramedButton
          :style="{'transform': 'translateX(' + normalTranslateX + 'px)'}"
          class="text-l mx-2 transition-transform pointer-events-auto"
          :fill="difficulty === 'normal'" :label="$t('normal')"
          @mousedown="setDifficulty('normal')"
        />
        <FramedButton
          :style="{'transform': 'translateX(' + hardTranslateX + 'px)'}"
          class="text-l ml-2 transition-transform pointer-events-auto"
          :fill="difficulty === 'hard'" :label="$t('hard')"
          @mousedown="setDifficulty('hard')"
        />
      </div>
      <div>
        <FramedButton
          :style="{'transform': 'translateX(' + playButtonTranslateX + 'px)'}"
          class="text-l transition-transform pointer-events-auto"
          color="orange" :fill="true" :label="$t('play')"
          @mousedown="play"
        />
      </div>
    </div>

    <div class="position-absolute d-flex flex-row justify-content-between w-100 pointer-events-none">
      <div class="text-l align-self-center">
        <div
          :style="{'transform': 'translateX(' + playWordTranslateX + 'px)'}"
          class="d-inline-block transition-transform"
        >{{ $t('play') }}</div>&nbsp;
        <div
          :style="{'transform': 'translateX(' + inTranslateX + 'px)'}"
          class="d-inline-block transition-transform"
        >{{ $t('in') }}</div>&nbsp;
        <div
          :style="{'transform': 'translateX(' + difficultyTranslateX + 'px)'}"
          class="d-inline-block transition-transform text-teal">{{ $t(difficulty) }}</div>
        <div
          :style="{'transform': 'translateX(' + questionMarkTranslateX + 'px)'}"
          class="d-inline-block transition-transform"
          v-html="$t('question_mark')"
        />
      </div>
      <div>
        <FramedButton
          :style="{'transform': 'translateX(' + yesTranslateX + 'px)'}"
          class="text-l mr-2 transition-transform pointer-events-auto" :fill="true" :label="$t('yes')"
          @mousedown="confirm"
        />
        <FramedButton
          :style="{'transform': 'translateX(' + noTranslateX + 'px)'}"
          class="text-l ml-2 transition-transform pointer-events-auto" :fill="false" :label="$t('no')"
          @mousedown="cancel"
        />
      </div>
    </div>

    <div class="position-absolute d-flex flex-row justify-content-between w-100 pointer-events-none">
      <div class="text-l align-self-center">
        <div :style="{'transform': 'translateX(' + sessionTimeTranslateX + 'px)'}">{{ formattedSessionTime }}</div>
      </div>
      <div>
        <FramedButton
          :style="{'transform': 'translateX(' + openTranslateX + 'px)'}"
          class="text-l mr-2 transition-transform pointer-events-auto" :fill="true" :label="$t('open_the_door')"
          @mousedown="open"
        />
      </div>
    </div>
  </div>
</template>

<script>
import FramedButton from '@/components/FramedButton.vue'
import businessStore from '@/store/businessStore.js'
import publishSubscribeService from '@/store/publishSubscribeService.js'

export default {
  name: "ButtonsBottom.vue",
  components: {
    FramedButton,
  },
  data() {
    return {
      difficulty: 'normal',
      areActionsLocked: false,
      easyTranslateX: 0,
      normalTranslateX: 0,
      hardTranslateX: 0,
      playButtonTranslateX: 0,
      playWordTranslateX: -1080,
      inTranslateX: -1080,
      difficultyTranslateX: -1080,
      questionMarkTranslateX: -1080,
      yesTranslateX: -1080,
      noTranslateX: -1080,
      openTranslateX: -1080,
      sessionTimeTranslateX: -1080,
    }
  },
  computed: {
    sessionTime() {
      return businessStore.state.sessionTime
    },
    formattedSessionTime() {
      if (this.sessionTime === null) {
        return "00:00"
      }

      function pad(num) {
        return ("0" + num).slice(-2);
      }

      var minutes = Math.floor(this.sessionTime / 60)
      var secs = Math.round(this.sessionTime % 60)
      var hours = Math.floor(minutes / 60)
      minutes = minutes % 60
      var time = pad(minutes) + ":" + pad(secs)

      if (hours > 9)
      {
        time = ">10h"
      } else if (hours > 0) {
        time = hours + ":" + time
      }

      return time
    }
  },
  methods: {
    setDifficulty(difficulty) {
      if (!this.areActionsLocked) {
        this.difficulty = difficulty
      }
    },
    play() {
      if (!this.areActionsLocked) {
        setTimeout(this.setData, 200, 'easyTranslateX', -1080)
        setTimeout(this.setData, 400, 'normalTranslateX', -1080)
        setTimeout(this.setData, 600, 'hardTranslateX', -1080)
        setTimeout(this.setData, 800, 'playButtonTranslateX', -1080)

        setTimeout(this.setData, 1400, 'playWordTranslateX', 0)
        setTimeout(this.setData, 1600, 'inTranslateX', 0)
        setTimeout(this.setData, 1800, 'difficultyTranslateX', 0)
        setTimeout(this.setData, 2000, 'questionMarkTranslateX', 0)
        setTimeout(this.setData, 2200, 'yesTranslateX', 0)
        setTimeout(this.setData, 2400, 'noTranslateX', 0)
      }
    },
    cancel() {
      if (!this.areActionsLocked) {
        setTimeout(this.setData, 200, 'playWordTranslateX', -1080)
        setTimeout(this.setData, 400, 'inTranslateX', -1080)
        setTimeout(this.setData, 600, 'difficultyTranslateX', -1080)
        setTimeout(this.setData, 800, 'questionMarkTranslateX', -1080)
        setTimeout(this.setData, 1000, 'yesTranslateX', -1080)
        setTimeout(this.setData, 1200, 'noTranslateX', -1080)

        setTimeout(this.setData, 1800, 'easyTranslateX', 0)
        setTimeout(this.setData, 2000, 'normalTranslateX', 0)
        setTimeout(this.setData, 2200, 'hardTranslateX', 0)
        setTimeout(this.setData, 2400, 'playButtonTranslateX', 0)
      }
    },
    confirm() {
      publishSubscribeService.commit('publish', {category: 'play'})

      this.areActionsLocked = true

      setTimeout(this.setData, 200, 'playWordTranslateX', -1080)
      setTimeout(this.setData, 400, 'inTranslateX', -1080)
      setTimeout(this.setData, 600, 'difficultyTranslateX', -1080)
      setTimeout(this.setData, 800, 'questionMarkTranslateX', -1080)
      setTimeout(this.setData, 1000, 'yesTranslateX', -1080)
      setTimeout(this.setData, 1200, 'noTranslateX', -1080)

      setTimeout(this.setData, 6000, 'openTranslateX', 0)
      setTimeout(this.setData, 6000, 'sessionTimeTranslateX', 0)
    },
    setData(key, value) {
      this[key] = value
    },
    open() {
      publishSubscribeService.commit('publish', {category: 'unlock_front_door'})
    },
  },
  watch: {
    sessionTime() {
      // No matter the current configuration step, everything is hidden except the session time that is displayed
      this.areActionsLocked = true
      this.easyTranslateX = -1080
      this.playWordTranslateX = -1080
      this.normalTranslateX = -1080
      this.hardTranslateX = -1080
      this.playButtonTranslateX = -1080
      this.playWordTranslateX = -1080
      this.inTranslateX = -1080
      this.difficultyTranslateX = -1080
      this.questionMarkTranslateX = -1080
      this.yesTranslateX = -1080
      this.noTranslateX = -1080
      this.openTranslateX = 0
      this.sessionTimeTranslateX = 0
    }
  }
}
</script>

<style scoped>
.frame {
  width: 980px;
}
</style>