<template>
  <div>
    <svg viewBox="0 0 118 51" class="mb-1">
      <g v-for="(v, index) in values" :key="v.id">
        <rect
          :x="v.x"
          :y="Math.abs(46 - (36 * v.percent / 100))"
          width="10"
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
      Nutrient market rates
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
          label: 'prote.',
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 22,
          percent: 70,
          label: 'proto.',
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 38,
          percent: 70,
          label: 'lip.',
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 54,
          percent: 27,
          label: 'gluc.',
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 70,
          percent: 89,
          label: 'mine.',
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 86,
          percent: 10,
          label: 'vit.',
          delta: '',
          deltaOpacity: 0,
          deltaColor: '#00d1b6',
        },
        {
          x: 102,
          percent: 29,
          label: 'a-ox.',
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
      // between -20.0% and +20.0%
      var newVariation = Math.floor(Math.random() * 400 - 200) / 10

      if (newVariation != 0) {
        if (
          this.values[valueIndex].percent * (1 + (newVariation / 100)) > 100 ||
          this.values[valueIndex].percent * (1 + (newVariation / 100)) < 0
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
          percent: this.values[valueIndex].percent * (1 + (newVariation / 100)),
          duration: 1000,
          easing: 'linear',
        }, 500)
      }

      setTimeout(this.variation, Math.random() * 6000 + 4000, valueIndex)
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
svg {
  height: 132px;
  width: 264px;
  border: 1px solid rgba(00, 209, 182, 0.4);
  box-shadow: 0px 0px 10px -6px rgba(0, 209, 182, 0.75);
}

.title {
  font-size: 12px;
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
