<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal-content">
      <div class="modal-header">
        <h2>{{ isEditing ? '编辑倒计时任务' : '创建倒计时任务' }}</h2>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </div>
      
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="taskName">任务名称</label>
          <input 
            id="taskName" 
            type="text" 
            v-model="formData.name"
            required
            placeholder="输入任务名称"
          >
        </div>
        
        <div class="form-group">
          <label for="deadline">截止日期</label>
          <input 
            id="deadline" 
            type="date" 
            v-model="formData.deadline"
            required
          >
        </div>
        
        <div class="form-group">
          <label for="backgroundImage">背景图片</label>
          <input 
            id="backgroundImage" 
            type="file" 
            @change="handleImageUpload"
            accept="image/*"
          >
          
          <div v-if="imagePreview" class="image-preview">
            <img :src="imagePreview" alt="背景图片预览">
          </div>
        </div>
        
        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="$emit('close')">取消</button>
          <button type="submit" class="submit-btn">{{ isEditing ? '保存更改' : '创建任务' }}</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CountdownTaskForm',
  props: {
    task: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      formData: {
        name: '',
        deadline: '',
        backgroundImage: null
      },
      imagePreview: null
    };
  },
  computed: {
    isEditing() {
      return !!this.task;
    }
  },
  watch: {
    task: {
      immediate: true,
      handler(newVal) {
        if (newVal) {
          this.formData.name = newVal.name;
          this.formData.deadline = newVal.deadline?.split('T')[0] || '';
          
          if (newVal.background_image_path) {
            const baseURL = import.meta.env.VITE_API_BASE_URL || '';
            this.imagePreview = `${baseURL}/${newVal.background_image_path}`;
          }
        }
      }
    }
  },
  methods: {
    handleImageUpload(event) {
      const file = event.target.files[0];
      if (!file) return;
      
      this.formData.backgroundImage = file;
      
      // 创建预览
      const reader = new FileReader();
      reader.onload = (e) => {
        this.imagePreview = e.target.result;
      };
      reader.readAsDataURL(file);
    },
    
    submitForm() {
      const formData = {
        name: this.formData.name,
        deadline: this.formData.deadline,
        backgroundImage: this.formData.backgroundImage
      };
      
      this.$emit('submit', formData);
    }
  }
};
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #666;
}

form {
  padding: 16px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input[type="text"],
input[type="date"] {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

input[type="file"] {
  width: 100%;
  padding: 10px 0;
}

.image-preview {
  margin-top: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  overflow: hidden;
  max-height: 200px;
}

.image-preview img {
  width: 100%;
  height: auto;
  object-fit: cover;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 20px;
}

button {
  padding: 10px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.cancel-btn {
  background-color: #f5f5f5;
  color: #333;
}

.submit-btn {
  background-color: #4caf50;
  color: white;
}

.submit-btn:hover {
  background-color: #388e3c;
}
</style> 