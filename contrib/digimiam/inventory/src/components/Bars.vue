<template>
  <div class="d-flex flex-column align-items-center w-100">
    <svg viewBox="0 0 118 51" class="px-3 py-2 glowing-container w-75 mb-1">
      <g v-for="(v, index) in values" :key="v.id">
        <rect
          :x="v.x"
          :y="Math.abs(46 - (36 * v.percent / 100))"
          width="13"
          :height="36 * v.percent / 100"
        />
        <foreignObject
          width="100%"
          height="100%"
          :x="getLabelX(index)"
          y="46"
        >
          <body xmlns="http://www.w3.org/1999/xhtml" class="bg-transparent">
            <div :id="'label-' + index" class="label">
              {{ v.label }}
            </div>
          </body>
        </foreignObject>
        <foreignObject
          width="100%"
          height="100%"
          :x="getDeltaX(index)"
          :y="Math.abs(46 - (36 * v.percent / 100)) - 3"
          :transform="'rotate(-45 ' + getDeltaX(index) + ' ' + (Math.abs(46 - (36 * v.percent / 100)) - 3) + ')'"
        >
          <body xmlns="http://www.w3.org/1999/xhtml" class="bg-transparent">
            <div :id="'delta-' + index" class="label diagonal" :style="{opacity: v.deltaOpacity, color: v.deltaColor}">
              {{ v.delta }}
            </div>
          </body>
        </foreignObject>
      </g>
    </svg>
    <div class="title text-center">
      {{ $t('nutrient_market_rates') }}
    </div>
  </div>
</template>

<script>
export default {
  name: 'Bars',
  data: function() {
    return {
      values: [
        {
          x: 6,
          percent: 50,
          label: this.$t('protein'),
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 25,
          percent: 70,
          label: this.$t('lipid'),
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 44,
          percent: 27,
          label: this.$t('carbohydrates'),
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 63,
          percent: 80,
          label: this.$t('vitamin'),
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 82,
          percent: 75,
          label: this.$t('mineral'),
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 101,
          percent: 78,
          label: this.$t('trace_mineral'),
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
      ]
    }
  },
  computed: {
   getLabelX: function() {
      return function(index) {
        var textElement = document.getElementById('label-' + index)
        if (textElement) {
          var textWidth = textElement.offsetWidth
          return (this.values[index].x + 5) - textWidth / 2
        } else {
          return this.values[index].x + 5
        }
      }
    },
    getDeltaX: function() {
      return function(index) {
        var textElement = document.getElementById('delta-' + index)
        if (textElement) {
          var textWidth = textElement.offsetWidth
          return (this.values[index].x + 5) - textWidth / 2
        } else {
          return this.values[index].x + 5
        }
      }
    },
  },
  methods: {
    variation: function(valueIndex) {
      // between -10.0 and +10.0
      var newVariation = Math.floor(Math.random() * 200 - 100) / 10

      if (newVariation != 0) {
        if (
          this.values[valueIndex].percent + newVariation > 100 ||
          this.values[valueIndex].percent + newVariation < 0
        ) {
          newVariation *= -1
        }

        this.values[valueIndex].delta = newVariation + '%'
        if (newVariation > 0) {
          this.values[valueIndex].deltaColor = '#00ff00'
          this.values[valueIndex].delta = '+' + newVariation + '%'
        } else if (newVariation < 0) {
          this.values[valueIndex].deltaColor = '#ff4500'
        }
        this.values[valueIndex].delta = this.values[valueIndex].delta[0] + this.values[valueIndex].delta.substring(1, this.values[valueIndex].delta.length)

        this.values[valueIndex].deltaOpacity = 1

        this.$anime.timeline({
          targets: this.values[valueIndex],
        }).add({
          deltaOpacity: 0,
          duration: 3000,
          easing: 'easeInExpo',
        }).add({
          percent: this.values[valueIndex].percent + newVariation,
          duration: 1000,
          easing: 'linear',
        }, 500)
      }

      setTimeout(this.variation, Math.random() * 60000 + 4000, valueIndex)
    }
  },
  mounted: function() {
    for (var i = 0 ; i < this.values.length ; i++) {
      // Triggers text centering
      this.values[i].x -= 1
      this.values[i].x += 1

      this.variation(i)
    }
  }
}
</script>

<style scoped>
.title {
  font-size: 16px;
}

rect {
  fill: rgb(0, 209, 182, 0.8);
}

.label {
  font-family: "Code New Roman";
  color: #00d1b6;
  font-size: 4px;
  display: inline-block;
  position: absolute;
  top: 0;
}
</style>
