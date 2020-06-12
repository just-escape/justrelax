<template>
  <div class="window d-flex flex-column" :style="{left: left, bottom: bottom, transform: transform}">
    <div class="d-flex flex-row rounded-top bg-info shadow-box-top align-items-center h-header">
      <Neons class="ml-2" color="var(--light)"/>
      <h3 class="size-12 py-1 mx-3 mb-0 text-white">{{ $t('information') }}</h3>
      <Neons class="mr-2" color="var(--light)"/>
    </div>
    <div class="border-left-bottom-right shadow-box-top bg-light-transparent p-3">
      <div class="media">
        <div class="mr-3 bg-info glow align-self-center d-flex justify-content-center align-items-center" style="width: 50px; height: 50px; border-radius: 50%">
          <i class="text-light size-17rem fas fa-info"></i>
        </div>
        <div class="media-body d-flex flex-column">
          <div class="mb-1">
            {{ $t('dear_customers') }}
            <br/>
            {{ $t('we_are_not_able_to_process_your_order') }}
          </div>
          <div class="mb-3">
            {{ $t('this_information_has_been_teletransmitted') }}
          </div>
          <b-btn
            variant="info"
            class="align-self-center py-2 px-5 mr-5"
            @click="$emit('ok')"
          >{{ $t('ok') }}</b-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Neons from "@/components/Neons.vue"

export default {
  name: "OrderNotification",
  components: {
    Neons,
  },
  data() {
    return {
      leftOffset: 200,
      bottomOffset: 300,
      scaleX: 0,
      scaleY: 0,
      animation: null,
    }
  },
  computed: {
    left() {
      return "calc(5% + " + this.leftOffset + "px)"
    },
    bottom() {
      return "calc(400px - " + this.bottomOffset + "px)"
    },
    transform() {
      return "scaleX(" + this.scaleX + ") scaleY(" + this.scaleY + ")"
    },
  },
  watch: {
    displayed(newValue) {
      if (newValue) {
        this.animation = this.$anime.timeline({
          targets: this,
        })
        .add({
          scaleX: 1,
          scaleY: 1,
          duration: 400,
          easing: 'easeInQuad'
        })
        .add({
          leftOffset: 0,
          bottomOffset: 0,
          duration: 700,
          easing: 'easeOutQuad'
        }, '-=700')
      } else {
        this.animation = this.$anime.timeline({
          targets: this,
        })
        .add({
          scaleX: 0,
          scaleY: 0,
          duration: 700,
          easing: 'easeInOutQuad'
        })
        .add({
          leftOffset: 200,
          bottomOffset: 300,
          duration: 400,
          easing: 'easeInOutQuad'
        }, '-=300')
      }
    },
  },
  created() {
  },
  props: {
    displayed: Boolean,
  }
}
</script>

<style scoped>
.window {
  width: 90%;
}

.h-header {
  height: 40px;
}

.bg-light-transparent {
  background: rgba(248, 249, 250, 0.65);
}

.border-left-bottom-right {
  border: 3px solid var(--info);
  border-top: 0px;
  border-bottom-left-radius: 0.25rem;
  border-bottom-right-radius: 0.25rem;
}

.glow {
  box-shadow: 0px 0px 3px var(--info);
}

.shadow-box-top {
  box-shadow: 1px -1px 5px var(--info);
}

.size-17rem {
  font-size: 1.7rem;
}
</style>
