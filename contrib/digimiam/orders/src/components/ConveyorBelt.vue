<template>
  <div class="position-relative" style="height: 100px; background-color: black; color: white">
    <div class="position-absolute d-flex flex-row justify-content-center align-items-center h-100 w-100">
      <ConveyorBeltChevron v-for="(c, index) in chevrons" :key="index" :blink="c.blink" class="chevron mx-3"/>
    </div>
  </div>
</template>

<script>
import ConveyorBeltChevron from '@/components/ConveyorBeltChevron'

export default {
  name: "ConveyorBelt",
  components: {
    ConveyorBeltChevron,
  },
  data() {
    return {
      chevrons: [
        {
          blink: false,
        },
        {
          blink: false,
        },
        {
          blink: false,
        },
        {
          blink: false,
        },
        {
          blink: false,
        },
        {
          blink: false,
        },
        {
          blink: false,
        },
      ]
    }
  },
  methods: {
    setChevronBlinking: function(chevronIndex) {
      this.chevrons[chevronIndex].blink = true
    }
  },
  mounted() {
    for (var i = 0 ; i < this.chevrons.length ; i++) {
      setTimeout(this.setChevronBlinking, i * 200, i)
    }
  },
}
</script>

<style scoped>
.chevron {
  font-size: 100px;
}
</style>
