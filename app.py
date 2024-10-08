from flask import Flask, render_template, jsonify
import psutil
import pynvml

app = Flask(__name__)

pynvml.nvmlInit()

def get_cpu_stats():
    cpu_usage = psutil.cpu_percent(interval=1)
    try:
        temps = psutil.sensors_temperatures()
        if 'coretemp' in temps:
            cpu_temp = temps['coretemp'][0].current
        else:
            cpu_temp = 'N/A'
    except Exception:
        cpu_temp = 'N/A'
    cpu_wattage = 'N/A'  
    return {
        'cpu_usage': cpu_usage,
        'cpu_temp': cpu_temp,
        'cpu_wattage': cpu_wattage
    }


def get_gpu_stats():
    handle = pynvml.nvmlDeviceGetHandleByIndex(0)
    gpu_utilization = pynvml.nvmlDeviceGetUtilizationRates(handle).gpu
    gpu_temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
    gpu_power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000 
    mem_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
    gpu_vram_usage = mem_info.used / (1024**2)

    return {
        'gpu_utilization': gpu_utilization,
        'gpu_temp': gpu_temp,
        'gpu_power_usage': gpu_power_usage,
        'gpu_vram_usage': gpu_vram_usage
    }
    

def get_memory_stats():
    memory_info = psutil.virtual_memory()
    return {
        'memory_usage': memory_info.percent
    }
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stats')
def stats():
    system_stats = {
        'cpu': get_cpu_stats(),
        'gpu': get_gpu_stats(),
        'memory': get_memory_stats()
    }
    return jsonify(system_stats)


if __name__ == '__main__':
    app.run(debug=True)
