<template>
  <div>
    <h2 class="big-noodle text-jaffa text-center">Timeline</h2>
    <b-card class="border-jaffa w-100 bgc-dark p-2" no-body>
      <div class="d-flex flex-row justify-content-end">
        <b-button-group class="mr-3">
          <ButtonJaffa size="sm" @click="strifeLeft()">
            <i class="fas fa-chevron-left fa-fw"></i>
          </ButtonJaffa>
          <ButtonJaffa size="sm" @click="strifeRight()">
            <i class="fas fa-chevron-right fa-fw"></i>
          </ButtonJaffa>
        </b-button-group>

        <b-button-group>
          <ButtonJaffa size="sm" @click="zoomIn()">
            <i class="fas fa-search-plus fa-fw"></i>
          </ButtonJaffa>
          <ButtonJaffa size="sm" @click="zoomReset()">
            <i class="fas fa-search fa-fw"></i>
          </ButtonJaffa>
          <ButtonJaffa size="sm" @click="zoomOut()">
            <i class="fas fa-search-minus fa-fw"></i>
          </ButtonJaffa>
        </b-button-group>
      </div>

      <div class="w-100">
        <svg :viewBox="viewBox">
          <line class="stroke-softdark" :x1="referenceLineX1" :x2="referenceLineX2" :y1="axisY" :y2="axisY" :style="styleStrokeWidth"/>

          <line
            v-if="getXFromTicks(currentTimeX) >= axisX1"
            :x1="ticksLineX1"
            :x2="ticksLineX2"
            :y1="axisY"
            :y2="axisY"
            class="stroke-jaffa"
            :style="styleStrokeWidth"
          />

          <g v-for="(t, index) in graduations" :key="t.id">
            <line
              class="stroke-jaffa"
              :x1="getXFromTicks(t)"
              :x2="getXFromTicks(t)"
              :y1="graduationLineY1"
              :y2="graduationLineY2"
              :style="styleStrokeWidth"
            />
            <foreignObject width="100%" height="100%" :x="getGraduationTextX(t, index)" :y="lowerTextY">
              <body xmlns="http://www.w3.org/1999/xhtml" class="bgc-dark">
                <div :id="'graduation' + index" :style="styleFontSize" class="timeline-text">
                  <TicksClock :ticks="t" :displayZero="true"/>
                </div>
              </body>
            </foreignObject>
          </g>

          <g id="records">
            <g v-for="record in records" :key="record.id" :id="record.id">
              <circle
                class="stroke-jaffa fill-jaffa"
                :cx="getXFromTicks(record.ticks)"
                :cy="axisY"
                :r="getProportionalValue(foregroundRecordId == record.id ? 15 : 10)"
                @mouseenter="sendRecordToForeground(record.id)"
                @mouseleave="sendRecordToBackground()"
              />
              <foreignObject
                width="100%"
                :height="upperTextHeight"
                :x="getUpperTextX(record.ticks)"
                :y="upperTextY"
                :transform="'rotate(-60 ' + getUpperTextX(record.ticks) + ' ' + upperTextY + ')'"
              >
                <body xmlns="http://www.w3.org/1999/xhtml" class="bgc-transparent position-relative">
                  <div
                    @mouseenter="sendRecordToForeground(record.id)"
                    @mouseleave="sendRecordToBackground()"
                  >
                    <div :style="styleFontSize" class="timeline-text">
                      {{ record.label }}
                    </div>
                  </div>
                </body>
              </foreignObject>
            </g>
          </g>
        </svg>
      </div>
    </b-card>
  </div>
</template>

<script>
import ButtonJaffa from '@/components/ButtonJaffa.vue'
import TicksClock from '@/components/TicksClock.vue'

export default {
  name: 'PageRoomTimeline',
  components: {
    ButtonJaffa,
    TicksClock,
  },
  data: function() {
    return {
      axisWidthDefault: 3600,
      axisX1: 0,
      axisX1Target: 0,
      axisX1Min: 0,
      axisX1Max: 6600, 
      axisX2: 3600,
      axisX2Target: 3600,
      axisX2Min: 600,
      axisX2Max: 7200,
      foregroundRecordId: null,
    }
  },
  computed: {
    pxPerTick: function() {
      return this.axisWidthDefault / 3600
    },
    axisWidth: function() {
      return this.axisX2 - this.axisX1
    },
    axisXMargin: function() {
      return this.getProportionalValue(80)
    },
    axisY: function() {
      return this.getProportionalValue(270)
    },
    viewBoxY: function() {
      return this.getProportionalValue(0)
    },
    viewBoxHeight: function() {
      return this.getProportionalValue(420)
    },
    upperTextY: function() {
      return this.getProportionalValue(230)
    },
    lowerTextY: function() {
      return this.getProportionalValue(300)
    },
    viewBox: function() {
      var x = this.axisX1 - this.axisXMargin
      var y = this.viewBoxY
      var width = this.axisWidth + 2 * this.axisXMargin
      var height = this.viewBoxHeight
      return x + ' ' + y + ' ' + width + ' ' + height
    },
    graduations: function() {
      var quarterWidth = this.axisWidth / 4
      var graduations = [
        this.axisX1,
        this.axisX1 + quarterWidth,
        this.axisX1 + quarterWidth * 2,
        this.axisX1 + quarterWidth * 3,
        this.axisX2,
      ]
      return graduations
    },
    records: function() {
      var r = this.room.liveData.records
        .filter(r => this.axisX1 <= this.getXFromTicks(r.ticks) && this.getXFromTicks(r.ticks) <= this.axisX2)
      return r
    },
    currentTimeX: function() {
      return this.room.ticks * this.pxPerTick
    },
    getXFromTicks: function() {
      return function(ticks) {
        return ticks * this.pxPerTick
      }
    },
    strifeOffset: function() {
      return (this.axisX2Target - this.axisX1Target) / 4 
    },
    styleStrokeWidth: function() {
      return {
        strokeWidth: this.getProportionalValue(10)
      }
    },
    styleFontSize: function() {
      return {
        fontSize: this.getProportionalValue(2.5) + 'rem',
        padding: this.getProportionalValue(0.5) + 'rem',
        borderRadius: this.getProportionalValue(0.8) + 'rem'
      }
    },
    upperTextHeight: function() {
      return this.getProportionalValue(2.5 + 2 * 0.5) + 'rem'
    },
    referenceLineX1: function() {
      return this.axisX1 - this.getProportionalValue(5)
    },
    referenceLineX2: function() {
      return this.axisX2 + this.getProportionalValue(5)
    },
    ticksLineX1: function() {
      return this.axisX1 - this.getProportionalValue(5)
    },
    ticksLineX2: function() {
      return Math.min(this.getXFromTicks(this.currentTimeX), this.axisX2) + this.getProportionalValue(5)
    },
    graduationLineY1: function() {
      return this.axisY - this.getProportionalValue(5)
    },
    graduationLineY2: function() {
      return this.axisY + this.getProportionalValue(15)
    },
    getUpperTextX: function() {
      return function(ticks) {
        return this.getXFromTicks(ticks) - this.getProportionalValue(25)
      }
    },
    getGraduationTextX: function() {
      return function(t, id) {
        var center = this.getXFromTicks(t)
        var textElement = document.getElementById('graduation' + id)
        if (textElement) {
          var textWidth = textElement.offsetWidth
          return center - textWidth / 2
        } else {
          return center
        }
      }
    },
    getProportionalValue: function() {
      return function(value) {
        return value * this.axisWidth / this.axisWidthDefault
      }
    }
  },
  methods: {
    sendRecordToForeground: function(recordId) {
      this.foregroundRecordId = recordId

      var recordsTag = document.getElementById('records')
      var recordTag = document.getElementById(recordId)
      recordsTag.appendChild(recordTag)
    },
    sendRecordToBackground: function() {
      this.foregroundRecordId = null
    },
    zoomIn: function() {
      var axisX2Offset = Math.min(600, this.axisX2Target - this.axisX1Target - 600)
      this.axisX2Target = this.axisX2Target - axisX2Offset
      this.$anime(
        {
          targets: this,
          axisX2: this.axisX2Target,
          duration: 500,
          easing: 'easeOutSine'
        }
      )
    },
    zoomOut: function() {
      var axisX2TargetTmp = Math.min(this.axisX2Max, this.axisX2Target + 600)
      var axisX1Offset = 600 - (axisX2TargetTmp - this.axisX2Target)
      this.axisX1Target = Math.max(this.axisX1Min, this.axisX1Target - axisX1Offset)
      this.axisX2Target = axisX2TargetTmp
      this.$anime(
        {
          targets: this,
          axisX1: this.axisX1Target,
          axisX2: this.axisX2Target,
          duration: 500,
          easing: 'easeOutSine'
        }
      )
    },
    zoomReset: function() {
      this.axisX1Target = 0
      this.axisX2Target = 3600
      this.$anime(
        {
          targets: this,
          axisX1: this.axisX1Target,
          axisX2: this.axisX2Target,
          duration: 500,
          easing: 'easeOutSine'
        }
      )
    },
    strifeLeft: function() {
      var offset = this.strifeOffset
      var x1Min = this.axisX1Min
      var x2Min = this.axisX1Min + (this.axisX2Target - this.axisX1Target)
      this.axisX1Target = Math.max(x1Min, this.axisX1Target - offset)
      this.axisX2Target = Math.max(x2Min, this.axisX2Target - offset)
      this.$anime(
        {
          targets: this,
          axisX1: this.axisX1Target,
          axisX2: this.axisX2Target,
          duration: 500,
          easing: 'easeOutSine'
        }
      )
    },
    strifeRight: function() {
      var offset = this.strifeOffset
      var x1Max = this.axisX2Max - (this.axisX2Target - this.axisX1Target)
      var x2Max = this.axisX2Max
      this.axisX1Target = Math.min(x1Max, this.axisX1Target + offset)
      this.axisX2Target = Math.min(x2Max, this.axisX2Target + offset)
      this.$anime(
        {
          targets: this,
          axisX1: this.axisX1Target,
          axisX2: this.axisX2Target,
          duration: 500,
          easing: 'easeOutSine'
        }
      )
    }
  },
  props: ['room'],
  mounted() {
    // Triggers lower text centering
    this.axisX1 = this.axisX1 + 1
    this.axisX2 = this.axisX2 + 1

    this.axisX1 = this.axisX1 - 1
    this.axisX2 = this.axisX2 - 1
  }
}
</script>

<style scoped>
.bgc-transparent {
  background: transparent;
}

.timeline-text {
  line-height: 1;
  color: #f8f9fa;
  font-family: "Lato", "Helvetica", "Arial", "sans-serif";
  display: inline-block;
  background-color: #4d4d4f;
  position: absolute;
  top: 0;
}

line {
  stroke-width: 10px;
}

.stroke-softdark {
  stroke: #4d4d4d;
}

.stroke-jaffa {
  stroke: #f38d40;
}

.fill-jaffa {
  fill: #f38d40;
}
</style>
